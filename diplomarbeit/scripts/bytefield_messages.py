
L = int("1000", 2)
R = int("0100", 2)
T = int("0010", 2)
B = int("0001", 2)

def _borderstr(border):
	return ("l" if (border & L) else "")\
		 + ("r" if (border & R) else "")\
		 + ("t" if (border & T) else "")\
		 + ("b" if (border & B) else "")

def cc(c = {}, add = {}, cpy = []):
	nc = {
		"border": (c["border"] & (T|L|R)) if c.has_key("border") else (T|L|R),
		"rwg": c["rwg"] if c.has_key("rwg") else True
	}
	for k, v in add.iteritems():
		nc[k] = v
	for k in cpy:
		if c.has_key(k):
			if add.has_key(k):
				nc[k] = c[k] + " \\\\ " + add[k]
			else:
				nc[k] = c[k]
	return nc

###

def bf(wordsize, content, title):
	return "\\begin{figure}[tbh]"\
		 + "\\begin{centering}"\
		 + "\\begin{bytefield}[bitwidth="+("%.1f" % (24.0 / wordsize))+"em]{"+str(wordsize)+"}"\
		 + " \\\\ \n"\
		 + "\\bitheader{0-"+str(wordsize-1)+"}"\
		 + " \\\\ \n"\
		 + content\
		 + "\\end{bytefield}"\
		 + "\\par\\end{centering}\n"\
		 + "\\protect\\caption{"+title+"}\n"\
		 + "\\end{figure}"

def con(*text):
	return " \\\\ \n".join(text)

###

def gen(part, proto, msgs, makegeneral = True):
	s = ""
	
	for msg in msgs:
		s += "\\newcommand{\\"+proto+msg+"t}{"+msgs[msg]+"}\n"
	
	s += "\n"
	
	for msg in msgs:
		s += "\\newcommand{\\"+proto+msg+"}{\\hyperref["+part+"-"+proto+"-"+msg+"]{\\"+proto+msg+"t}}\n"
	
	s += "\n"
	if makegeneral:
		s += "\\newcommand{\\"+proto+"bytefield}{"+bf(8, eval(proto)(), "\\gls*{"+proto+"} -- Genereller Messageaufbau")+"}\n"
	
	for msg in msgs:
		s += "\n\\newcommand{\\"+proto+msg+"bytefield}{"+bf(8, eval(proto+msg)(), "\\gls*{"+proto+"} -- \\msg{\\"+proto+msg+"t}")+"}"
	
	return s

###

def rwg(c, name, text, desc):
	if c["rwg"] == True or c["rwg"].count(name) > 0:
		text = "\\begin{rightwordgroup}{"+desc+"}\n"\
			 + text + "\n"\
			 + "\\end{rightwordgroup}\n"
	return text

###

def varlen(c):
	return "\\wordbox["+_borderstr(c["border"]&(L|R|T))+"]{2}{"+c["desc"]+"} \\\\ \n"\
		 + "\\skippedwords \\\\ \n"\
		 + "\\wordbox["+_borderstr(c["border"]&(L|R|B))+"]{1}{}\n"

def fixlen(c):
	content = ""
	if c.has_key("desc"):
		content += c["desc"]
	if c.has_key("val"):
		if len(content) > 0:
			content += " (\\code{"+c["val"]+"})"
		else:
			content += "\\code{"+c["val"]+"}"
	return "\\wordbox["+_borderstr(c["border"])+"]{1}{"+content+"}\n"

###

def byte(c):
	return fixlen(cc(c, {}, ["border", "val", "desc"]))

def flexnum(c):
	return varlen(cc(c, {"desc": "\\flexnumfield"}, ["border", "desc"]))

def array(c):
	return con(flexnum(cc(c, {"desc": "Element Count"})), rwg(c, c["rwgid"], c["content"], c["name"]), rwg(c, c["rwgid"], varlen(cc(c, {"desc": "$\\cdots$"}, ["border"])), c["name"]))

def lla(c):
	return con(flexnum(cc(c, {"desc": "\\acrshort{lla} Type"})), varlen(cc(c, {"desc": "\\acrshort{lla} Data \\\\ $N$ Bytes"}, ["border"])))

def llalist(c):
	return array(cc(c, {"rwgid": "llalist", "name": "\\acrshort{lla}", "content": lla(cc(c))}, ["border"]))

def key(c):
	return con(byte(cc(c, {"desc": "Key Type"})), varlen(cc(c, {"desc": "Key Data \\\\ $N$ Bytes"}, ["border"])))

def data(c):
	return con(flexnum(cc(c, {"desc": (c["desc"] if c.has_key("desc") else "Data") + " Length"})), varlen(cc(c, {"desc": "Data, $N$ Bytes"}, ["border", "desc"])))

def string(c):
	return con(varlen(cc(c, {"desc": "ASCII String Data, $N$ Bytes"}, ["desc"])), byte(cc(c, {"desc": "String Delimiter", "val": "0"}, ["border"])))

def nettype(c):
	return string(cc(c, {"desc": "Network Type Descriptor"}, ["border"]))

def netpkt(c):
	return varlen(cc(c, {"desc": "\\netpktfield"}, ["border", "desc"]))

###

def _isinit(i, c = {}):
	return rwg(cc(), "", byte(cc(c, {"val": str(i)}, ["border"])), "Message Type")

def isproto():
	return con(flexnum(cc({}, {"desc": "Message Type"})), varlen(cc({}, {"border": T|B|L|R, "desc": "Message Data \\\\ $N$ Bytes"})))

def isprotoversion():
	return con(_isinit(0), flexnum(cc({}, {"border": T|B|L|R, "desc": "Version"})))

def isprotollareq():
	return con(_isinit(1), flexnum(cc({}, {"border": T|B|L|R, "desc": "Limit"})))

def isprotollarep():
	return con(_isinit(2), llalist(cc({}, {"border": T|B|L|R, "rwg": ["llalist"]})))

def isprotots():
	return con(_isinit(3), flexnum(cc({}, {"desc": "Address Slot"})), rwg(cc(), "", key(cc({}, {"border": T|B|L|R})), "Address Key"))

def isprotoccreq():
	return con(_isinit(4), flexnum(cc({}, {"desc": "Address Slot"})), rwg(cc(), "", data(cc({}, {"border": T|B|L|R})), "Challenge Data"))

def isprotoccrep():
	return con(_isinit(5), flexnum(cc({}, {"desc": "Address Slot"})), rwg(cc(), "", data(cc({}, {"border": T|B|L|R})), "Signed Data"))

def isprotocbn():
	return con(_isinit(6), flexnum(cc({}, {"desc": "Address Slot"})), byte(cc({}, {"border": T|B|L|R, "desc": "Connection Base"})))

def isprotonjn():
	return con(_isinit(7), flexnum(cc({}, {"desc": "Address Slot"})), flexnum(cc({}, {"desc": "Network Slot"})), rwg(cc(), "", nettype(cc({}, {"border": T|B|L|R})), "Network Type"))

def isprotonln():
	return con(_isinit(8), flexnum(cc({}, {"desc": "Address Slot"})), flexnum(cc({}, {"desc": "Network Slot", "border": T|B|L|R})))

def isprotoireq():
	return _isinit(9, {"border": T|B|L|R})

def isprotoicreq():
	return con(_isinit(10), rwg(cc(), "", lla(cc({}, {"border": T|B|L|R})), "Remote Address"))

def isprotonp():
	return con(_isinit(13), flexnum(cc({}, {"desc": "Network Slot"})), rwg(cc(), "", netpkt(cc({}, {"border": T|B|L|R})), "Network Packet"))

def isprotoacsa():
	return con(_isinit(14), flexnum(cc({}, {"desc": "Application Channel Slot"})), flexnum(cc({}, {"desc": "Sender Address Slot"})), flexnum(cc({}, {"desc": "Receiver Address Slot"})), string(cc({}, {"desc": "Action Identifier", "border": T|B|L|R})))

def isprotoacd():
	return con(_isinit(15), flexnum(cc({}, {"desc": "Application Channel Slot"})), data(cc({}, {"desc": "Application Channel Data", "border": T|B|L|R})))

###

ISPROTO = {
	"version": "Version",
	"llareq": "LLA Request",
	"llarep": "LLA Reply",
	"ts": "Trusted Switch",
	"ccreq": "Crypto Challenge Request",
	"ccrep": "Crypto Challenge Reply",
	"cbn": "Connection Base Notice",
	"njn": "Network Join Notice",
	"nln": "Network Leave Notice",
	"ireq": "Integration Request",
	"icreq": "Integration Reply",
	"np": "Network Packet",
	"acsa": "Application Channel Slot Assign",
	"acd": "Application Channel Data"
}

print(gen("dcl", "isproto", ISPROTO))



