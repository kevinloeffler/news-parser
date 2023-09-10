import csv
from datetime import datetime, date
from bs4 import BeautifulSoup
from typing import Callable

from util import load_html, save_crawled_pages, extract_date


def get_pages(filename: str) -> list[str]:
    pages = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            pages.append(row[0])
    return pages


def get_pages_with_range(filename: str, start: int, stop: int) -> list[str]:
    pages = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        row_count = 1

        # go to start row
        for _ in reader:
            if row_count == start:
                break
            row_count += 1

        for row in reader:
            if row_count > stop:
                break
            row_count += 1
            pages.append(row[0])
            # yield row[0]
    return pages


def date_parser_nzz(url: str) -> date:
    html_document = load_html(url)
    doc = BeautifulSoup(html_document, features='html.parser')
    time_tag = doc.find('time')
    date_time = datetime.strptime(time_tag['datetime'], '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_time.date()


def date_parser_20min(url: str) -> date:
    html_document = load_html(url)
    doc = BeautifulSoup(html_document, features='html.parser')
    time_tag = doc.find('time')
    date_time = datetime.strptime(time_tag['datetime'], '%Y-%m-%dT%H:%M:%S%z')
    return date_time.date()


def date_parser_badener_tagblatt(url: str) -> date:
    html_document = load_html(url)
    doc = BeautifulSoup(html_document, features='html.parser')
    time_tag = doc.find('time')
    date_time = extract_date(time_tag['datetime'])
    return date_time


def date_parser_basler_zeitung(url: str) -> date:
    html_document = load_html(url)
    doc = BeautifulSoup(html_document, features='html.parser')
    time_tag = doc.find('time')
    date_time = extract_date(time_tag['datetime'])
    return date_time


def find_pages_in_daterange(start_date: date,
                            end_date: date,
                            pages: list[str],
                            date_parser: Callable[[str], date]) -> list[str]:
    start_index = find_date(target_date=start_date, start_index=0, pages=pages, date_parser=date_parser)
    end_index = find_date(target_date=end_date, start_index=start_index, pages=pages, date_parser=date_parser)
    return pages[start_index: end_index + 1]


def find_date(target_date: date,
              start_index: int,
              pages: list[str],
              date_parser: Callable[[str], date]) -> int:
    step_sizes = [100_000, 10_000, 1_000, 100, 10]
    index = start_index

    # find the closest date to target date
    for step_size in step_sizes:
        if step_size > (index + len(pages)):
            continue  # prevent index out of range errors

        index = find_biggest_date_index_before_target_date(
            target_date=target_date,
            start_index=index,
            pages=pages,
            step_size=step_size,
            date_parser=date_parser
        )

    # find the target date
    while date_parser(pages[index]) < target_date:
        index += 1

    return index


def find_biggest_date_index_before_target_date(target_date: date,
                                               start_index: int,
                                               pages: list[str],
                                               step_size: int,
                                               date_parser: Callable[[str], date]) -> int:
    index = start_index

    while date_parser(pages[index]) < target_date:
        index += step_size
        if index > len(pages):
            break  # prevent index out of range
    return index - step_size


def run_crawler():
    pages = get_pages('sitemaps/Badener_Tagblatt.csv')
    reversed_pages = list(reversed(pages))

    START_DATE = date(2018, 10, 1)
    END_DATE = date(2020, 1, 1)

    pages_in_daterange = find_pages_in_daterange(start_date=START_DATE,
                                                 end_date=END_DATE,
                                                 pages=reversed_pages,
                                                 date_parser=date_parser_badener_tagblatt)

    print(f'found {len(pages_in_daterange)} pages')
    save_crawled_pages(pages_in_daterange, 'Badener_Tagblatt')


# run_crawler()

'''
pages = get_pages('sitemaps/NZZ.csv', 1, 10)
dates: list[date] = []

start_time = datetime.now()
for page in pages:
    document = load_html(page)
    dates.append(date_parser_nzz(document))
end_time = datetime.now()

print(dates)
print('time per page:', (end_time - start_time) / (len(dates)))
'''
