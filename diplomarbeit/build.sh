#!/bin/sh

pdflatex diplomarbeit

echo
echo
echo
echo -n "press enter to continue"
read void

makeindex -c -q "diplomarbeit.idx"
bibtex diplomarbeit
makeglossaries diplomarbeit
pdflatex diplomarbeit
pdflatex diplomarbeit
