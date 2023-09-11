from parser import parser_freiburger
from runner import run_parser
from util import sort_and_merge_parser_result


def parse_freiburger_nachrichten():
    result_file = run_parser('Freiburger_Nachrichten.pkl', parser=parser_freiburger)
    sort_and_merge_parser_result(path_to_parser_result=result_file, path_to_output_file='results/Freiburger_Nachrichten.csv')
