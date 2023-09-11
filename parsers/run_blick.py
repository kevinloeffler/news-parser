from parser import parser_blick
from runner import run_parser
from util import sort_and_merge_parser_result


# DOES NOT WORK!

def parse_blick():
    result_file = run_parser('Blick.pkl', parser=parser_blick)
    sort_and_merge_parser_result(path_to_parser_result=result_file, path_to_output_file='results/Blick.csv')
