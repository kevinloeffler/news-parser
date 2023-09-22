from parser import parser_sg_tagblatt
from runner import run_parser
from util import sort_and_merge_parser_result


def parse_sg_tagblatt():
    result_file = run_parser('SG_Tagblatt.pkl', parser=parser_sg_tagblatt)
    sort_and_merge_parser_result(path_to_parser_result=result_file, path_to_output_file='results/SG_Tagblatt.csv')
