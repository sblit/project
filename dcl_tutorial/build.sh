#!/bin/sh

if egrep -r "\\\-[a-z]" dcl_tutorial.tex; then
	echo "looks like there are wrong hyphenations";
	echo "\n\nfailed\n\n"
	exit 1
fi

(
	pdflatex dcl_tutorial &&
#	makeindex -c -q "dcl_tutorial.idx" &&
	pdflatex dcl_tutorial &&
	pdflatex dcl_tutorial &&
	echo -e "\n\ndone\n\n"
) || (
	echo -e "\n\nfailed\n\n"
)
