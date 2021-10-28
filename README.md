# extract_phonenum

## Usage
`./extract_phonenum.py [-h] path [path ...]`
- `-h`: for usage help
- `-path`: file path to be extracted

## Description
Extract phone number with optional contry code from a given text file. Ouput the extracted phone
number line by line to stdout.

## Known Issues

* country code should start with `+` symobl, limit from 1~3 digits.
* If country is provided, then area code is limit to exactly 2 digits.
* Otherwise, area code should be exactly 3 digits follows by two set of 4 digits phone numbers.

# ensg2hugo

## Usage
* download `Homo_sapiens.GRCh37.75.gtf` first, `wget http://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/Homo_sapiens.GRCh37.75.gtf.gz`
`./ensg2hugo.py [-h] path [path ...]`
- `-h`: for usage help
- `-path`: file path to be replaced

## Description
A script to generate mapping of Ensembl name to HUGO name and then replcae input tsv/csv with reference to the mapping.

## Known Issues

# histogram

## Install
`pip install -r requriements.txt`

## Usage
`usage: histogram.py [-h] [-f F] path`
- `-h`: for usage help.
- `-path`: tsv file path to be plot.
- `-f {0-9} | -f{0-9}`: specify the column number to be plot, cound contains spaces in between.

## Description
Plot histogram from tsv file, save with the name `histogram.png`.
* The tsv file should includes a header row to indicate the representation of each column. 

## Known Issues

### Limitations
* This program is limited to process tsv file with row count less than 100.
* colum specified from `-f` option should not exceed the max column size of the input tsv.
