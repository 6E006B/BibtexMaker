#!/usr/bin/env python

import re
from sets import Set

LATEXCITEREGEX = re.compile("\\cite(?:\[[^]]*\])?{([^}]+)}", re.M | re.I | re.S)
BIBCITEREGEX = re.compile("@[^{]+{([^,]+),", re.M | re.I | re.S)
CITETEMPLATE = """
@%s{%s,
AUTHOR="",
TITLE="",
YEAR=
}
"""

def getCitesForLatexFile(f):
    cites = Set()
    for cite in LATEXCITEREGEX.findall(open(f).read()):
        cites.add(cite)
    return cites

def getCitesForBibFile(f):
    cites = Set()
    for cite in BIBCITEREGEX.findall(open(f).read()):
        cites.add(cite.strip())
    return cites


def createBibtexFile(outfile, cites, citeType, replace):
    mode = "w" if replace else "a"
    fh = open(outfile, mode)
    for cite in cites:
        writeCitation(fh, cite, citeType)
    fh.close()

def writeCitation(fh, cite, citeType):
    fh.write(CITETEMPLATE % (citeType, cite))

if __name__=="__main__":

    import argparse

    parser = argparse.ArgumentParser(description="create a prefilled bibtex file from latex documents")
    parser.add_argument('files', metavar="FILE", type=str, nargs="+", help="LaTeX files to parse for citations")
    parser.add_argument('-o', '--outfile', dest="outfile", type=str, default="bibtex.bib", help="output file for the bibtex (default: bibtex.bib)")
    parser.add_argument('-b', '--bib', dest="bibs", type=str, default=[], action="append", help="bib files to check for already defined references")
    parser.add_argument('-t', '--type', dest="citeType", type=str, default="BOOK", help="define the type of citation for the Bibtex file (default: BOOK)")
    parser.add_argument('-r', '--replace', dest="replace", action="store_true", default=False, help="replace the outfile if it exists (default: append to outfile)")
    args = parser.parse_args()

    neededCites = Set()
    for f in args.files:
        neededCites.update(getCitesForLatexFile(f))
    definedCites = Set()
    for f in args.bibs:
        definedCites.update(getCitesForBibFile(f))
    cites = neededCites - definedCites
    createBibtexFile(args.outfile, cites, args.citeType, args.replace)
