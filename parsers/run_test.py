import time
from datetime import datetime
from typing import Union

from runner import run_parser
from util import sort_and_merge_parser_result

test_dates = ['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-02', '2023-01-01']


def test_parser(url: str) -> Union[dict[str, datetime.date, dict[str, int]], None]:
    print(f'parsing url: {url}')
    time.sleep(1)
    return {'date': test_dates.pop(0), 'match': {'klimastreik': 0, 'klima': 1, 'streik': 0}}


def parse_test():
    result_file = run_parser('test.pkl', parser=test_parser)
    sort_and_merge_parser_result(path_to_parser_result=result_file, path_to_output_file='results/test.csv')
