import csv
import concurrent.futures
from datetime import datetime
from typing import Callable, Union

from util import load_crawled_pages, create_new_parser_result_file

MAX_THREAD_COUNT = 128


def run_parser(crawled_pages_filename: str, parser: Callable[[str], Union[dict[str, datetime.date, dict[str, int]], None]]) -> str:
    start_time = datetime.now()

    filename = crawled_pages_filename[:-4] if crawled_pages_filename.endswith('.pkl') else crawled_pages_filename

    print(f'start parsing {filename}...')
    pages = load_crawled_pages(filename)

    result_file = create_new_parser_result_file(name=filename)

    with open(result_file, 'a', newline='') as file:
        writer = csv.writer(file)

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREAD_COUNT) as executor:
            future_to_item = {executor.submit(parser, page): page for page in pages}

            for future in concurrent.futures.as_completed(future_to_item):
                item = future_to_item[future]
                print('item:', item)
                try:
                    result = future.result()
                    if result is not None:
                        writer.writerow([result['date']] + [value for _, value in result['match'].items()])
                except Exception as error:
                    print(error)

    end_time = datetime.now()
    print(f'parsed {len(pages)} pages in {end_time - start_time} seconds = {(end_time - start_time) / len(pages)} seconds per page')

    return result_file
