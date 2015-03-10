import math

offset = 0;

for n in range(9):
	vals = (1 << (max(7-n, 0) + 8*n));
	print("\\code{%s} & $%d$ -- $%d$ & $%d$ & $%s\\%%$\\tabularnewline\n\\hline" % (
		("1" * n) + (("0" + ("X" * (7-n))) if n < 8 else ""),
		offset,
		offset + vals - 1,
		n,
		("%.2f" % (100 * math.log(offset + vals, 2) / (8*(n+1)))).replace(".", ",")
	));
	offset += vals;

