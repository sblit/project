#!/bin/sh

(
	pdflatex dcl_tutorial &&
#	makeindex -c -q "dcl_tutorial.idx" &&
	pdflatex dcl_tutorial &&
	pdflatex dcl_tutorial &&
	echo -e "\n\ndone\n\n"
) || (
	echo -e "\n\nfailed\n\n"
)
