#!/usr/bin/env python3
import argparse
import csv
import logging
import logging.handlers
import os
import re
import sys
from typing import Dict, List

GTF_FILE = 'Homo_sapiens.GRCh37.75.gtf'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_arg():

    def dir_path(path):
        if os.path.isfile(path):
            return path
        else:
            raise argparse.ArgumentTypeError(
                f"readable_dir:{path} is not a valid file or does not exists")

    def column_type(x):
        x = int(x)
        if x < 0 or x > 9:
            raise argparse.ArgumentTypeError("column should between 0 to 9")
        return x

    parser = argparse.ArgumentParser(
        description='Lookup the Ensembl name and replace it with the HUGO name.')
    parser.add_argument(
        'path',  help='path of file which needs replacement.', type=dir_path)
    parser.add_argument(
        '-f',   default=2,  help='future option', type=column_type)
    args = parser.parse_args()
    if not args.path:
        parser.error('Please provide file to be replace.')
    return args


def parse_gtf() -> Dict:
    mapping = dict()

    with open(GTF_FILE, 'r') as tsv:
        for line in csv.reader(tsv, delimiter="\t"):
            if len(line) < 9:
                continue
            match = re.search(
                r'gene_id "(.+?)";.*gene_name "(.+?)";', line[8])

            gene_id, gene_name = match.group(1), match.group(2)
            mapping[gene_id] = gene_name
    return mapping


def format_header(header: List) -> str:
    header[0] = 'id'
    header = ','.join(header)
    return header.replace('gene_id', 'gene_name')


if __name__ == '__main__':
    args = parse_arg()
    # logger.debug(f'file path: {args.path}')
    # logger.debug(f'-f : {args.f}')

    mapping = parse_gtf()
    with open(args.path, 'r') as csv_file:
        rows = csv.DictReader(csv_file)

        print(format_header(rows.fieldnames))

        for row in rows:
            row_list = []
            for k, v in row.items():
                if(k == 'gene_id'):
                    word_before_dot = re.search(r'(\w+).', v).group(1)
                    if v != mapping.get(word_before_dot, v):
                        pass
                        # logger.debug(
                        #     f'word_before_dot: {word_before_dot} orig_v: {v}, new_v:{mapping.get(word_before_dot, v)}')
                    row_list.append(mapping.get(word_before_dot, v))
                else:
                    row_list.append(v)
            print(','.join(row_list))
