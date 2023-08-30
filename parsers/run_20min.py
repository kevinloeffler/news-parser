from datetime import datetime

from parser import merge_same_days, safe_parser_output, parser_20min
from util import load_crawled_pages, create_new_parser_result_file


def parse_20min():
    start_time = datetime.now()

    print('start parsing 20min...')
    pages = load_crawled_pages('20min')

    result_file = create_new_parser_result_file(name='20min')
    parser_results = []

    for page in pages:
        result = parser_20min(page)
        if result is None:
            # skip empty results
            continue

        if len(parser_results) == 0 or parser_results[-1]['date'] == result['date']:
            parser_results.append(result)
        else:
            merged_parser_results = merge_same_days(parser_results)
            safe_parser_output(merged_parser_results, filename=result_file)
            parser_results = []

    end_time = datetime.now()
    print(f'parsed {len(pages)} pages in {end_time - start_time} seconds = {(end_time - start_time) / len(pages)} seconds per page')

'''
    parser_result = []
    for page in pages:
        res = parser_nzz(page)
        parser_result.append(res)

    merged_parser_output = merge_same_days(parser_result)
    safe_parser_output(merged_parser_output, 'NZZ')

    end_time = datetime.now()
    print(f'parsed {len(pages)} pages in {end_time - start_time} seconds = {(end_time - start_time) / len(pages)} seconds per page')
'''