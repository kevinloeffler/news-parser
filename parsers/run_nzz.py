from datetime import datetime

from parser import parser_nzz, merge_same_days, safe_parser_output
from util import load_crawled_pages


def parse_nzz():
    print('start parsing NZZ...')
    pages = load_crawled_pages('NZZ')

    start_time = datetime.now()

    parser_result = []
    for page in pages:
        res = parser_nzz(page)
        parser_result.append(res)

    merged_parser_output = merge_same_days(parser_result)
    safe_parser_output(merged_parser_output, 'NZZ')

    end_time = datetime.now()
    print(f'parsed {len(pages)} pages in {end_time - start_time} seconds = {(end_time - start_time) / len(pages)} seconds per page')
