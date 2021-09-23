#!/usr/bin/env python3

# 6:22 a.m
import os
import re
import sys
import subprocess
import argparse
import logging
import logging.handlers
import matplotlib.pyplot as plt
import pandas as pd

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_arg():

    def dir_path(path): 
        if os.path.isfile(path): 
            return path 
        else: 
            raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid file or does not exists")

    def column_type(x):
        x = int(x)
        if x < 0 or x > 9:
            raise argparse.ArgumentTypeError("column should between 0 to 9")
        return x

    parser = argparse.ArgumentParser(description='Parse phone numbers from file.')
    parser.add_argument('path',  help='path of file which used for generating histogram png.', type=dir_path)
    parser.add_argument('-f',   default=2,  help='plot histogram from which column, default: col 2', type=column_type)
    args = parser.parse_args()    
    if not args.path:
        parser.error('Please provide file to be extracted.')
    return args

def plot(file_path, which_col):
    data = pd.read_csv(file_path, sep='\t', skiprows=[0], header=None)
    
    if (data.shape[1] < which_col):
        raise Exception(f'{file_path} has {data.shape[1]} columns,  {which_col} is out of the index')

    selected_data = data.iloc[:, [which_col-1]]
    logger.debug(f'selected_data: {selected_data}')
    selected_data.plot(kind='bar')
    plt.ylabel('y-value')
    plt.xlabel('x-value')
    plt.title('histogram plot')
    plt.savefig('histogram.png')

if __name__ == '__main__':
    args = parse_arg()
    logger.debug(f'file path: {args.path}')
    logger.debug(f'-f : {args.f}')
    plot(args.path, args.f+1)
