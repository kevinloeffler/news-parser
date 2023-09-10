from parser import parser_badener_tagblatt
from runner import run_parser
from util import sort_and_merge_parser_result


def parse_badener_tagblatt():
    result_file = run_parser('Badener_Tagblatt.pkl', parser=parser_badener_tagblatt)
    sort_and_merge_parser_result(path_to_parser_result=result_file, path_to_output_file='results/Badener_Tagblatt.csv')
