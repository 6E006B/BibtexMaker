#!/usr/bin/env python

import re
from sets import Set

CITEREGEX = re.compile("\\cite{([^}]+)}", re.M | re.I | re.S)
CITETEMPLATE = """
@BOOK{%s,
AUTHOR="",
TITLE="",
YEAR=,
}
"""

def getCitesForFile(f):
    cites = Set()
    for cite in CITEREGEX.findall(open(f).read()):
        if not cite in cites:
            cites.add(cite)
    return cites

def createBibtexFile(outfile, cites):
    fh = open(outfile, "w+")
    for cite in cites:
        writeCitation(fh, cite)
    fh.close()

def writeCitation(fh, cite):
    fh.write(CITETEMPLATE % cite)

if __name__=="__main__":

    import argparse

    parser = argparse.ArgumentParser(description="create a prefilled bibtex file from latex documents")
    parser.add_argument('files', metavar="FILE", type=str, nargs="+", help="LaTeX files to parse for citations")
    parser.add_argument('-o', '--outfile', dest="outfile", type=str, default="bibtex.bib", help="output file for the bibtex (default: bibtex.bib)")
    args = parser.parse_args()

    cites = Set()
    for f in args.files:
        cites.update(getCitesForFile(f))
    createBibtexFile(args.outfile, cites)
