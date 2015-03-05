#!/bin/sh

pdflatex diplomarbeit &&
makeindex -c -q "diplomarbeit.idx" &&
bibtex diplomarbeit &&
makeglossaries diplomarbeit &&
pdflatex diplomarbeit &&
pdflatex diplomarbeit
