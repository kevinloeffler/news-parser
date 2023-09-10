from datetime import datetime

from parser import parser_20min
from runner import run_parser
from util import sort_and_merge_parser_result


def parse_20min():
    result_file = run_parser('30min.pkl', parser=parser_20min)
    sort_and_merge_parser_result(path_to_parser_result=result_file, path_to_output_file='results/30min.csv')
