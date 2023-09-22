import re
from datetime import datetime
import csv
from bs4 import BeautifulSoup
from util import load_html, extract_date
from typing import Union

TARGET_WORDS = ['klimastreik', 'klima', 'streik']


def find_words(text: str, words: list[str]) -> dict[str, int]:
    result: dict[str, int] = {word: 0 for (word) in words}
    for t in text.split(' '):
        for word in words:
            if word in t:
                result[word] = 1
    return result


def parser_nzz(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    # helper function
    def extract_content(result: list):
        if len(result) == 0:
            return ''
        return result[0].text

    try:
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
    except:
        return None


def parser_20min(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    def extract_content(element) -> str:
        if element[0]:
            return element[0].text
        return ''

    try:
        html_document = load_html(url)
        document = BeautifulSoup(html_document, features='html.parser')

        # parse date
        time_tag = document.find('time')
        date_time = datetime.strptime(time_tag['datetime'], '%Y-%m-%dT%H:%M:%S%z')
        date = date_time.date()

        # parse text
        raw_title = document.find(name='div', class_='Article_elementTitle')
        raw_title = document.select('[class*=Article_elementTitle]')
        title = extract_content(raw_title)
        raw_lead = document.find(name='div', class_='Article_elementLead')
        raw_lead = document.select('[class*=Article_elementLead]')
        lead = extract_content(raw_lead)
        raw_article = document.find(name='section', class_='Article_body')
        raw_article = document.select('[class*=Article_body]')
        article = extract_content(raw_article).lower()

        full_text = title + ' ' + lead + ' ' + article
        matched_words = find_words(text=full_text, words=TARGET_WORDS)
        return {'date': date, 'match': matched_words}
    except:
        return None


def parser_badener_tagblatt(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    def extract_content(element) -> str:
        if element:
            return element.text.lower()
        return ''

    try:
        html_document = load_html(url)
        document = BeautifulSoup(html_document, features='html.parser')

        # parse date
        time_tag = document.find('time')
        date = extract_date(time_tag['datetime'])

        # parse text
        raw_article = document.find(name='div', class_='article')
        article = extract_content(raw_article)

        matched_words = find_words(text=article, words=TARGET_WORDS)
        return {'date': date, 'match': matched_words}
    except:
        return None


def parser_basler_zeitung(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    def extract_content(element) -> str:
        if element:
            return element.text.lower()
        return ''

    try:
        html_document = load_html(url)
        document = BeautifulSoup(html_document, features='html.parser')

        # parse date
        time_tag = document.find('time')
        date = extract_date(time_tag['datetime'])

        # parse text
        raw_article = document.find(name='div', class_='article')
        article = extract_content(raw_article)

        matched_words = find_words(text=article, words=TARGET_WORDS)
        return {'date': date, 'match': matched_words}
    except:
        return None


def parser_berner_zeitung(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    def extract_content(element) -> str:
        if element:
            return element.text.lower()
        return ''

    try:
        html_document = load_html(url)
        document = BeautifulSoup(html_document, features='html.parser')

        # parse date
        time_tag = document.find('time')
        date = extract_date(time_tag['datetime'])

        # parse text
        raw_article = document.find(name='article')
        article = extract_content(raw_article)

        matched_words = find_words(text=article, words=TARGET_WORDS)
        return {'date': date, 'match': matched_words}
    except:
        return None


def parser_blick(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    def extract_content(element) -> str:
        if element:
            return element.text.lower()
        return ''

    try:
        html_document = load_html(url)
        document = BeautifulSoup(html_document, features='html.parser')
        x = document.text[0]

        # parse date
        raw_date = document.find_all(string=re.compile('Publiziert: (\d*\.\d*\.\d*)', flags=re.I))[0]
        date_array = re.findall('Publiziert: (\d*)\.(\d*)\.(\d*)', raw_date)[0]
        date = datetime(int(date_array[2]), int(date_array[1]), int(date_array[0])).date()
        print('date:', date)
        if date is None:
            return None

        # parse text
        raw_header = document.find(name='div', class_='bAlVHo')
        header = extract_content(raw_header)
        raw_text = document.find(name='article')
        text = extract_content(raw_text)

        full_text = header + ' ' + text
        matched_words = find_words(text=full_text, words=TARGET_WORDS)
        return {'date': date, 'match': matched_words}

    except Exception as error:
        print(error)
        return None


def parser_freiburger(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    def extract_content(element) -> str:
        if element:
            return element.text.lower()
        return ''

    try:
        html_document = load_html(url)
        document = BeautifulSoup(html_document, features='html.parser')

        # parse date
        time_wrapper = document.find(name='span', class_='elementor-post-info__item--type-date')
        date_string_array = time_wrapper.text.split('\n')
        date_string = date_string_array[2].strip()
        date = datetime.strptime(date_string, '%d.%m.%Y').date()

        # parse text
        raw_title = document.find(name='h1')
        title = extract_content(raw_title)
        raw_text = document.find(name='div', class_='elementor-widget-theme-post-content')
        text = extract_content(raw_text)
        raw_paywall_text = document.find(name='div', class_='elementor-widget-theme-post-excerpt')
        paywall_text = extract_content(raw_paywall_text)

        full_text = title + ' ' + text + ' ' + paywall_text
        matched_words = find_words(text=full_text, words=TARGET_WORDS)
        return {'date': date, 'match': matched_words}

    except Exception as error:
        print(error)
        return None


def parser_luzerner(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    def extract_content(element) -> str:
        if element:
            return element.text.lower()
        return ''

    try:
        html_document = load_html(url)
        document = BeautifulSoup(html_document, features='html.parser')

        # parse date
        time_tag = document.find('time')
        date = extract_date(time_tag['datetime'])

        # parse text
        raw_article = document.find(name='section', class_='container--article')
        article = extract_content(raw_article)

        matched_words = find_words(text=article, words=TARGET_WORDS)
        return {'date': date, 'match': matched_words}

    except Exception as error:
        print(error)


def parser_sg_tagblatt(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    def extract_content(element) -> str:
        if element:
            return element.text.lower()
        return ''

    try:
        html_document = load_html(url)
        document = BeautifulSoup(html_document, features='html.parser')

        # parse date
        time_tag = document.find('time')
        date = extract_date(time_tag['datetime'])

        # parse text
        raw_article = document.find(name='section', class_='container--article')
        article = extract_content(raw_article)

        matched_words = find_words(text=article, words=TARGET_WORDS)
        return {'date': date, 'match': matched_words}

    except Exception as error:
        print(error)


'''
def merge_same_days_with_booleans(parser_output: list[dict[str, datetime.date, dict[str, bool]]]) -> list[dict[str, datetime.date, dict[str, int]]]:
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


def merge_same_days(parser_output: list[dict[str, datetime.date, dict[str, int]]]) -> list[dict[str, datetime.date, dict[str, int]]]:
    output = iter(parser_output)

    first_element = next(output)
    matches_of_first_element = {key: value for key, value in first_element['match'].items()}
    merged_output = [{'date': first_element['date'], 'match': matches_of_first_element}]
    print(merged_output)

    for row in output:
        if merged_output[-1]['date'] == row['date']:
            for key, value in merged_output[-1]['match'].items():
                merged_output[-1]['match'][key] += row['match'][key]
        else:
            merged_output.append(row)
    return merged_output


def sort_and_merge_results(input_file_path: str, output_file_name: str):
    with open(input_file_path, 'r') as file:
        reader = csv.reader(file)

        with open(f'final_results/{output_file_name}', 'x') as new_file:
            writer = csv.writer(new_file)
            writer.writerow(next(reader))

            unmerged_list = []
            for row in reader:
                item = {'date': row[0], 'match': {'klimastreik': int(row[1]), 'klima': int(row[2]), 'streik': int(row[3])}}
                unmerged_list.append(item)

            sorted_list = merge_same_days(unmerged_list)

            for row in sorted_list:
                writer.writerow([row['date']] + [value for _, value in row['match'].items()])
'''


def safe_parser_output(parser_output: list[dict[str, datetime.date, dict[str, int]]], filename: str):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        for row in parser_output:
            writer.writerow([row['date']] + [value for _, value in row['match'].items()])
            print(f'wrote date {row["date"]} to {filename}')
