#!/bin/sh

(
	pdflatex diplomarbeit &&
	makeindex -c -q "diplomarbeit.idx" &&
	bibtex diplomarbeit &&
	makeglossaries diplomarbeit &&
	pdflatex diplomarbeit &&
	pdflatex diplomarbeit &&
	echo -e "\n\ndone\n\n"
) || (
	echo -e "\n\nfailed\n\n"
)
