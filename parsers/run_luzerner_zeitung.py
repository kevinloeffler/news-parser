from parser import parser_luzerner
from runner import run_parser
from util import sort_and_merge_parser_result


def parse_luzerner_zeitung():
    result_file = run_parser('Luzerner_Zeitung.pkl', parser=parser_luzerner)
    sort_and_merge_parser_result(path_to_parser_result=result_file, path_to_output_file='results/Luzerner_Zeitung.csv')
