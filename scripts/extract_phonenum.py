#!/usr/bin/env python3

# 11:35 p.m
import os
import re
import sys
import subprocess
import argparse
import logging
import logging.handlers

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_arg():

    def dir_path(path): 
        if os.path.isfile(path): 
            return path 
        else: 
            raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid file or does not exists")

    parser = argparse.ArgumentParser(description='Parse phone numbers from file.')
    parser.add_argument('path', nargs='+', help='path of file which may contains phone numbers.', type=dir_path)
    args = vars(parser.parse_args())
    if not any(args.values()):
        parser.error('Please provide file to be extracted.')
    return args

def extract(path):
    phone_patt = r"\+?\b[\d]{1,3}-[\d]{2}-[\d]{4}-[\d]{4}|\b[\d]{2,3}-[\d]{3}-[\d]{4}"

    matched = []

    with open(path, "r") as f:
        for line in f:
            matched += re.findall(phone_patt, line)
            logger.debug(f'line: {line}')
            logger.debug(f'matched: {matched}')

    return matched

def converter(numbers):
    res = []
    for num in numbers:
        part = num.split('-')
        if num.startswith('+'):
            logger.debug('in start with country code')
            country_code = part[0]
            area_code = '(' + part[1] + ')'
            others = ''.join(part[2:])
        else:
            country_code = ''
            area_code = '(' + part[0] + ')'
            others = ''.join(part[1:])

        joined = ' '.join([country_code, area_code, others])
        res.append(joined)

    return res 

if __name__ == '__main__':
    args = parse_arg()
    logger.debug(f"path is {args.get('path')[0]}")
    matched_numbers = extract(args.get('path')[0])

    formatted_numbers = converter(matched_numbers)

    for num in formatted_numbers:
        print(num)
