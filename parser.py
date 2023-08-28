from datetime import datetime
import csv
from bs4 import BeautifulSoup
from util import load_html, load_crawled_pages, create_unique_filename

TARGET_WORDS = ['klimastreik', 'klima', 'streik']


def find_words(text: str, words: list[str]) -> dict[str, bool]:
    result: dict[str, bool] = {word: False for (word) in words}
    for t in text.split(' '):
        for word in words:
            if word in t:
                result[word] = True
    return result


def parser_nzz(url: str) -> dict[str, datetime.date, dict[str, bool]]:
    # helper function
    def extract_content(result: list):
        if len(result) == 0:
            return ''
        return result[0].text

    html_document = load_html(url)
    document = BeautifulSoup(html_document, features='html.parser')

    # parse date
    time_tag = document.find('time')
    date_time = datetime.strptime(time_tag['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
    date = date_time.date()

    # parse text
    raw_title = document.find_all(name="h1", class_='headline__title')
    title = extract_content(raw_title)
    raw_lead = document.find_all(name='p', class_='headline__lead')
    lead = extract_content(raw_lead)
    raw_article = document.find_all(name='p', class_='articlecomponent')
    article = extract_content(raw_article)
    full_text = (title + ' ' + lead + ' ' + article).lower()

    matched_words = find_words(text=full_text, words=TARGET_WORDS)
    return {'date': date, 'match': matched_words}


def merge_same_days(parser_output: list[dict[str, datetime.date, dict[str, bool]]]) -> list[dict[str, datetime.date, dict[str, bool]]]:
    output = iter(parser_output)

    first_element = next(output)
    matches_of_first_element = {key: (1 if value else 0) for key, value in first_element['match'].items()}
    merged_output = [{'date': first_element['date'], 'match': matches_of_first_element}]

    for row in output:
        if merged_output[-1]['date'] == row['date']:
            for key, value in merged_output[-1]['match'].items():
                merged_output[-1]['match'][key] += row['match'][key]
        else:
            merged_output.append(row)
    return merged_output


def safe_parser_output(parser_output: list[dict[str, datetime.date, dict[str, bool]]], name: str):
    filename = create_unique_filename(f'results/{name.replace(" ", "_")}', suffix='.csv')
    with open(filename, 'x', newline='') as file:
        writer = csv.writer(file)

        header_row = ['date'] + [key for key in parser_output[0]['match']]
        writer.writerow(header_row)

        for row in parser_output:
            writer.writerow([row['date']] + [value for _, value in row['match'].items()])

'''
pages = load_crawled_pages('NZZ')
test_pages = pages[0: 100]

start_time = datetime.now()
parser_result = []
for page in test_pages:
    res = parser_nzz(page)
    parser_result.append(res)
    for key, value in res.items():
        print(f'{key}: {value}')
end_time = datetime.now()
merged_parser_output = merge_same_days(parser_result)
safe_parser_output(merged_parser_output, 'NZZ')
print(f'parsed {len(test_pages)} pages in {end_time - start_time} seconds = {(end_time - start_time) / len(test_pages)} seconds per page')
'''
