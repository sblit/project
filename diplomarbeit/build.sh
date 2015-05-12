#!/bin/sh

if [ "--force" != "$1" ]; then

	if grep --color -ir "\\.}" content/*_glossary.tex; then
		echo "\n\nERROR: don't end glossary descriptions with a dot\nnot built\nuse --force to override\n\n"
		if [ "--test" != "$1" ]; then
			exit 1
		fi
	fi

	if egrep --color -ir "section{.*\\\\gls.*}" content/*.tex; then
		echo "\n\nERROR: don't use \\gls{...} in any sections\nnot built\nuse --force to override\n\n"
		if [ "--test" != "$1" ]; then
			exit 1
		fi
	fi

	if egrep --color -ir "caption{.*\\\\gls[^\\*].*}" content/*.tex; then
		echo "\n\nERROR: use \\gls*{...} only in captions\nnot built\nuse --force to override\n\n"
		if [ "--test" != "$1" ]; then
			exit 1
		fi
	fi

fi

if [ "--test" = "$1" ]; then
	exit 0
fi

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
