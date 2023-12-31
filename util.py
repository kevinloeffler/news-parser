import csv
import pickle
from datetime import datetime, date

import requests
from os import path


def extract_date(date_string: str) -> date:
    date_formats = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%fZ']

    for date_format in date_formats:
        try:
            date_time = datetime.strptime(date_string, date_format)
            return date_time.date()
        except ValueError as error:
            continue

    raise ValueError(f'time data "{date_string}" does not match any format')


def load_html(url: str) -> str:
    response = requests.get(url)
    return response.text


def save_crawled_pages(crawled_pages: list[str], filename):
    with open('crawled-pages/' + filename + '.pkl', 'wb') as output:
        pickle.dump(crawled_pages, output, pickle.HIGHEST_PROTOCOL)


def load_crawled_pages(filename: str) -> list[str]:
    with open('crawled-pages/' + filename + '.pkl', 'rb') as input_file:
        return pickle.load(input_file)


def create_unique_filename(filename: str, suffix: str) -> str:
    if not path.exists(filename + suffix):
        return filename + suffix
    index = 1
    while path.exists(filename + f'_{index}' + suffix):
        index += 1
    return filename + f'_{index}' + suffix


def create_new_parser_result_file(name: str) -> str:
    filename = create_unique_filename(f'parser-results/{name}'.replace(" ", "_"), '.csv')
    with open(filename, 'x', newline='') as file:
        writer = csv.writer(file)
        header_row = ['date', 'klimastreik', 'klima', 'streik']
        writer.writerow(header_row)

    return filename


def sort_and_merge_parser_result(path_to_parser_result: str, path_to_output_file: str):
    with open(path_to_output_file, 'x') as output_file:
        writer = csv.writer(output_file)

        with open(path_to_parser_result, 'r') as input_file:
            reader = csv.reader(input_file)

            header_row = next(reader)
            writer.writerow(header_row)

            parser_result = []
            for row in reader:
                parser_result.append({
                    'date': datetime.strptime(row[0], '%Y-%m-%d').date(),
                    'match': {'klimastreik': int(row[1]), 'klima': int(row[2]), 'streik': int(row[3])}
                })

            sorted_parser_result = sort_parser_result(parser_result)
            merged_parser_result = merge_parser_result(sorted_parser_result)

            for result in merged_parser_result:
                writer.writerow([
                    result['date'],
                    result['match']['klimastreik'],
                    result['match']['klima'],
                    result['match']['streik']
                ])


def sort_parser_result(parser_result: list[dict[str, any, dict[str, int]]]) -> list[dict[str, any, dict[str, int]]]:
    start_date = date(2018, 10, 1)
    end_date = date(2020, 1, 1)
    filtered_parser_result = filter(lambda row: start_date <= row['date'] <= end_date, parser_result)
    return sorted(filtered_parser_result, key=lambda row: row['date'])


def merge_parser_result(sorted_parser_result: list[dict[str, any, dict[str, int]]]) -> list[dict[str, any, dict[str, int]]]:
    merged_list = [sorted_parser_result[0]]

    for row in sorted_parser_result[1:]:
        if merged_list[-1]['date'] == row['date']:
            for key, value in merged_list[-1]['match'].items():
                merged_list[-1]['match'][key] += row['match'][key]
        else:
            merged_list.append(row)

    return merged_list
