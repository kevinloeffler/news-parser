from parser import parser_berner_zeitung
from runner import run_parser
from util import sort_and_merge_parser_result


def parse_berner_zeitung():
    result_file = run_parser('Berner_Zeitung.pkl', parser=parser_berner_zeitung)
    sort_and_merge_parser_result(path_to_parser_result=result_file, path_to_output_file='results/Berner_Zeitung.csv')
