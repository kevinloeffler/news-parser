from parser import parser_basler_zeitung
from runner import run_parser
from util import sort_and_merge_parser_result


def parse_basler_zeitung():
    result_file = run_parser('Basler_Zeitung.pkl', parser=parser_basler_zeitung)
    sort_and_merge_parser_result(path_to_parser_result=result_file, path_to_output_file='results/Basler_Zeitung.csv')
