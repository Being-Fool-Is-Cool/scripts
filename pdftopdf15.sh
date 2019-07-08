#!/bin/sh
# file: pdftopdf15.sh
# vim:fileencoding=utf-8:fdm=marker:ft=sh
#
# Copyright © 2014-2016 R.F. Smith <rsmith@xs4all.nl>.
# SPDX-License-Identifier: MIT
# Created: 2014-02-27T00:15:14+0100
# Last modified: 2019-07-08T17:09:15+0200

if [ $# -lt 1 ]; then
    echo "Usage: $(basename $0) file"
    exit 1
fi

# Check for special programs that are used in this script.
PROGS="gs"
for P in $PROGS; do
    which $P >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "$(basename $0): The program \"$P\" cannot be found."
        exit 1
    fi
done

for f in "$@"; do
    echo "Processing file \"$f\""
    TMPNAME=$(mktemp)
    INNAME=$f
    gs -DNOPAUSE -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 \
        -sOutputFile=$TMPNAME "${INNAME}" -c quit >/dev/null 2>&1
    mv "$INNAME" "${INNAME%.pdf}-orig.pdf"
    cp $TMPNAME "${INNAME}"
    rm -f $TMPNAME
done
