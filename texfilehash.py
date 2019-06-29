#!/usr/bin/env python3
# file: texfilehash.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Copyright © 2019 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2019-06-28T16:13:39+0200
# Last modified: 2019-06-29T17:55:17+0200
"""
Create a file containing the abbreviated git commit hash for TeX source files.
If the file has uncommitted changes, it appends the status in red text.
It produces a file <filename>.hash for every <filename>.tex.
"""
import argparse
import subprocess
import logging
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '--log',
    default='warning',
    choices=['debug', 'info', 'warning', 'error'],
    help="logging level (defaults to 'warning')"
)
parser.add_argument(
    'filenames', nargs='*', metavar='filename', help='TeX files to process'
)
args = parser.parse_args(sys.argv[1:])
logging.basicConfig(
    level=getattr(logging, args.log.upper(), None), format='%(levelname)s: %(message)s'
)

for infn in args.filenames:
    logging.debug(f'processing file {infn}')
    if not infn.endswith('.tex'):
        logging.error(f'{infn} is not a TeX file; skipping')
        continue  # Skip.

    outfn = infn[:-4] + '.hash'

    logcmd = ['git', '--no-pager', 'log', '-1', '--pretty=format:%h', sys.argv[1]]
    logdata = subprocess.check_output(logcmd).decode('ascii')
    logging.debug(f'logdata: "{logdata}"')

    statcmd = ['git', '--no-pager', 'status', '-s', '--', sys.argv[1]]
    statdata = subprocess.check_output(statcmd)[:2].decode('ascii').strip()
    logging.debug(f'statdata: "{statdata}"')

    if statdata:
        logdata = logdata + r'\,\textcolor{red}{' + statdata + r'}%'
        logging.info(f'{infn} has unrecorded changes')
    else:
        logdata += '%'

    with open(outfn, 'wt') as outf:
        outf.write(logdata)
        logging.info(f'wrote "{outfn}"')
else:
    logging.warning('no filenames given')
