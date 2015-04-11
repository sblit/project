# coding=utf-8

import sys

EMPTY = sys.argv.count("--empty") > 0
HEADINGS = sys.argv.count("--headings") > 0

def parseprotocols():
	protocols = []
	n = False
	for arg in sys.argv:
		if arg == "--protocols":
			n = True
			continue
		if n:
			if arg == "*":
				return True
			else:
				protocols += arg.split(",")
			n = False
	return protocols;

WRITEPROTOCOLS = parseprotocols()

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
		"rwg": c["rwg"] if c.has_key("rwg") else True,
		"varlensize": c["varlensize"] if c.has_key("varlensize") else 3,
		"size": c["size"] if c.has_key("size") else 1,
		"flexnumstyle": c["flexnumstyle"] if c.has_key("flexnumstyle") else "normal"
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

def bf(wordsize, content, title, label):
	if EMPTY: return ""
	return "\\begin{figure}"\
		 + "\\begin{centering}"\
		 + "\\begin{bytefield}[bitwidth="+("%.1f" % (18.0 / wordsize))+"em]{"+str(wordsize)+"}"\
		 + " \\\\ \n"\
		 + "\\bitheader{0-"+str(wordsize-1)+"}"\
		 + " \\\\ \n"\
		 + content\
		 + "\\end{bytefield}"\
		 + "\\par\\end{centering}"\
		 + "\\protect\\caption{"+title+"}"\
		 + "\\label{"+label+"}"\
		 + "\\end{figure}"

def con(*text):
	return " \\\\ \n".join(text)

###

def gen(part, proto, info, makegeneral = True):
	s = ""

	msgs = info["messages"]
	latexname = info["latexname"]
	gentext = info["gentext"] if info.has_key("gentext") else (latexname + " -- Genereller Messageaufbau")
	typecmd = info["type"] if info.has_key("type") else "\\msg"

	for msg in msgs:
		s += "\\newcommand{\\"+proto+msg+"t}{"+msgs[msg]+"}\n"

	s += "\n"

	for msg in msgs:
		s += "\\newcommand{\\"+proto+msg+"}{\\hyperref["+part+"-"+proto+"-"+msg+"]{\\"+proto+msg+"t}}\n"

	s += "\n"
	if makegeneral:
		s += "\\newcommand{\\"+proto+"bytefield}{"+bf(8, eval(proto)(), gentext, part+"-"+proto+"-bytefield")+"}\n"

	for msg in msgs:
		s += "\n\\newcommand{\\"+proto+msg+"bytefield}{"+bf(8, eval(proto+msg)(), latexname + " -- " + typecmd + "{\\"+proto+msg+"t}", part+"-"+proto+"-"+msg+"-bytefield")+"}"

	return s

def genheadings(part, proto, info, makegeneral = True):
	s = ""

	msgs = info["messages"]

	if makegeneral:
		s += "\\subsection{Messageaufbau}\nTODO\n\n\\"+proto+"bytefield\n\n"

	s += "\\subsection{Messages}\n\n"

	for msg in msgs:
		s += "\\subsubsection{"+msgs[msg]+"}\n\\label{"+part+"-"+proto+"-"+msg+"}\nTODO\n\n\\"+proto+msg+"bytefield\n\n\n"

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
	# with vdots
	content = ""
	if c.has_key("desc"):
		content += c["desc"]
	if c["varlensize"] > len(content) or c["varlensize"] > (content.count("\\\\") + 1):
		if len(content) > 0:
			content += " \\\\ "
		content += "$\\vdots$"
	return "\\wordbox["\
		+ _borderstr(c["border"])\
		+ "]{"\
		+ str(c["varlensize"])\
		+ "}{"\
		+ content\
		+ "}\n"
	# with skippedwords:
	#descp = c["desc"].split("\\\\", 1)
	#tdesc = descp[0]
	#bdesc = descp[1] if len(descp) > 1 else ""
	#return "\\wordbox["+_borderstr(c["border"]&(L|R|T))+"]{1}{"+tdesc+"} \\\\ \n"\
	#	 + "\\skippedwords \\\\ \n"\
	#	 + "\\wordbox["+_borderstr(c["border"]&(L|R|B))+"]{1}{"+bdesc+"}\n""""

def fixlen(c):
	content = ""
	if c.has_key("desc"):
		content += c["desc"]
	if c.has_key("val"):
		if len(content) > 0:
			content += " (\\code{"+c["val"]+"})"
		else:
			content += "\\code{"+c["val"]+"}"
	return "\\wordbox["+_borderstr(c["border"])+"]{"+str(c["size"])+"}{"+content+"}\n"

###

def byte(c):
	return fixlen(cc(c, {}, ["border", "val", "desc"]))

def flexnum(c):
	return varlen(cc(c, {"desc": "\\flexnumfield", "varlensize": 2 if c.has_key("flexnumstyle") and c["flexnumstyle"] == "short" else 3}, ["border", "desc"]))

def array(c):
	return con(flexnum(cc(c, {"desc": (c["name"] if c.has_key("name") else "Element") + " Count"})), rwg(c, c["rwgid"], c["content"], c["name"]), rwg(c, c["rwgid"], varlen(cc(c, {"varlensize": 1}, ["border"])), c["name"]))

def lla(c):
	return con(flexnum(cc(c, {"desc": (c["desc"] if c.has_key("desc") else "\\acrshort{lla}") + " Type"})), varlen(cc(c, {"desc": (c["desc"] if c.has_key("desc") else "\\acrshort{lla}") + " Data \\\\ $N$ Bytes"}, ["border"])))

def llalist(c):
	return array(cc(c, {"rwgid": "llalist", "name": "\\acrshort{lla}", "content": lla(cc(c))}, ["border"]))

def key(c):
	return con(byte(cc(c, {"desc": (c["desc"] if c.has_key("desc") else "Key") + " Type"})), varlen(cc(c, {"desc": "Key Data, $N$ Bytes"}, ["desc", "border"])))
	#return con(byte(cc(c, {"desc": "Key Type"})), varlen(cc(c, {"desc": "Key Data \\\\ $N$ Bytes"}, ["border"])))

def data(c):
	return con(flexnum(cc(c, {"desc": (c["desc"] if c.has_key("desc") else "Data") + " Length"})), varlen(cc(c, {"desc": "Data, $N$ Bytes"}, ["border", "desc"])))

def fixdata(c):
	return varlen(cc(c, {"desc": "Data, "+str(c["size"])+" Bytes"}, ["border", "desc"]))

def string(c):
	return con(varlen(cc(c, {"desc": "ASCII String Data, $N$ Bytes"}, ["desc"])), byte(cc(c, {"desc": "String Delimiter", "val": "0"}, ["border"])))

def nettype(c):
	return string(cc(c, {"desc": "Network Type Descriptor"}, ["border"]))

def netpkt(c):
	return varlen(cc(c, {"desc": "\\netpktfield"}, ["border", "desc"]))

def netslot(c = {}):
	return flexnum(cc(c, {"desc": "Network Slot"}, ["border", "desc"]))

def netendpslot(c = {}):
	return flexnum(cc(c, {"desc": "Network Endpoint Slot"}, ["border", "desc"]))

def appchslot(c = {}):
	return flexnum(cc(c, {"desc": "Application Channel Slot"}, ["border", "desc"]))

def cryptoinitid(c = {}):
	return flexnum(cc(c, {"desc": "Crypto Init Identifier"}, ["border", "desc"]))

def cryptoinitidlist(c = {}):
	return array(cc(c, {"rwgid": "cryptoinitidlist", "name": "Crypto Init Identifier", "content": cryptoinitid(cc(c))}, ["border"]))

def channelid(c = {}):
	return flexnum(cc(c, {"desc": "\\gls{channelid}"}, ["border", "desc"]))

def channelidlist(c = {}):
	return array(cc(c, {"rwgid": "channelidlist", "name": "\\gls{channelid}", "content": channelid(cc(c))}, ["border"]))

def dataid(c = {}):
	return flexnum(cc(c, {"desc": (c["desc"]+" " if c.has_key("desc") else "") + "\\gls{dataid}"}, ["border"]))

def dataidlist(c = {}):
	return array(cc(c, {"rwgid": "dataidlist", "name": (c["desc"]+" " if c.has_key("desc") else "") + "\\gls{dataid}", "content": dataid(cc(c))}, ["border"]))

def idblock(c = {}):
	return con(dataid(cc(c, {"desc": "Start"})), flexnum(cc(c, {"desc": "Inner Size"}, ["border"])))

def idblocklist(c = {}):
	return array(cc(c, {"rwgid": "idblocklist", "name": (c["desc"]+" " if c.has_key("desc") else "") + "Data ID Block", "content": idblock(cc(c))}, ["border"]))

def channelreport(c = {}):
	return con(channelid(cc(c)), dataid(cc(c, {"desc": "Lowest"})), dataid(cc(c, {"desc": "Highest"})), flexnum(cc(c, {"desc": "Total Number of \\glspl{dataid}"})), dataidlist(cc(c, {"desc": "Missing"})), idblocklist(cc(c, {"desc": "Missing"}, ["border"])))

def channelreportlist(c = {}):
	return array(cc(c, {"rwgid": "channelreportlist", "name": "Channel Report", "content": channelreport(cc(c))}, ["border"]))

def bigint(c = {}):
	return con(flexnum(cc(c, {"desc": (c["desc"]+" " if c.has_key("desc") else "") + "BigInteger Data Length"})), varlen(cc(c, {"desc": (c["desc"]+" " if c.has_key("desc") else "") + "BigInteger Data"}, ["border"])))

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

def _asinit(i, c = {}):
	return rwg(cc(), "", byte(cc(c, {"val": str(i)}, ["border"])), "Message Type")

def asproto():
	return con(byte(cc({}, {"desc": "Message Type"})), varlen(cc({}, {"border": T|B|L|R, "desc": "Message Data \\\\ $N$ Bytes"})))

def asprotorevision():
	return con(_asinit(0), flexnum(cc({}, {"border": T|B|L|R, "desc": "Revision"})))

def asprotogenkey():
	return con(_asinit(1, {"border": T|B|L|R}))

def asprotojoinnet():
	return con(_asinit(2), rwg(cc(), "", nettype(cc({}, {"border": T|B|L|R})), "Network Type"))

def asprotoslotassign():
	return con(_asinit(3), netendpslot(), rwg(cc(), "", nettype(cc({}, {"border": T|B|L|R})), "Network Type"), varlen(cc({}, {"border": T|B|L|R, "desc": "Address Data \\\\ $N$ Bytes"})))

def asprotodata():
	return con(_asinit(4), netendpslot(), data(cc({}, {"desc": "Address Data", "border": T|B|L|R})), data(cc({}, {"desc": "Message Data", "border": T|B|L|R})))

def asprotoaddrpubkey():
	return con(_asinit(5), key({"desc": "Address Public Key", "border": T|B|L|R}))

def asprotojoindefnets():
	return con(_asinit(6, {"border": T|B|L|R}))

def asprotokeyenc():
	return con(_asinit(7), data(cc({}, {"desc": "Plain Data", "border": T|B|L|R})))

def asprotokeydec():
	return con(_asinit(8), data(cc({}, {"desc": "Encrypted Data", "border": T|B|L|R})))

def asprotocryptoresponse():
	return con(_asinit(9), data(cc({}, {"desc": "Response Data", "border": T|B|L|R})))

def asprotoappchoutreq():
	return con(_asinit(10), netendpslot(), appchslot(), string({"desc": "Action Identifier"}), key({"desc": "Remote Public Key", "border": T|B|L|R}))

def asprotoappchinreq():
	return con(_asinit(11), netendpslot(), string({"desc": "Action Identifier"}), key({"desc": "Remote Public Key"}), lla({"desc": "Sender LLA"}), data({"desc": "Ignore Data", "border": T|B|L|R}))

def asprotoappchaccept():
	return con(_asinit(12), netendpslot(), appchslot(), string({"desc": "Action Identifier"}), key({"desc": "Remote Public Key"}), lla({"desc": "Sender LLA"}), data({"desc": "Ignore Data", "border": T|B|L|R}))

def asprotoappchconnected():
	return con(_asinit(13), appchslot({"border": T|B|L|R}))

def asprotoappchdata():
	return con(_asinit(14), appchslot(), data({"desc": "Application Channel Data", "border": T|B|L|R}))

def asprotokeyencblocksizereq():
	return con(_asinit(15, {"border": T|B|L|R}))

def asprotokeynum():
	return con(_asinit(16), flexnum({"desc": "Key Response Number", "border": T|B|L|R}))

###

def crisp():
	return con(byte({"desc": "Revision"}), byte({"desc": "Message Type"}), varlen(cc({}, {"border": T|B|L|R, "desc": "Message Data \\\\ $N$ Bytes"})))

def crispneighreq():
	return con(byte({"desc": "Revision", "val": "0"}), byte({"desc": "Message Type", "val": "0"}), string({"desc": "Action Identifier"}), lla({"desc": "Sender LLA"}), byte({"desc": "Response Flag"}), data({"desc": "Ignore Data", "border": T|B|L|R}))

###

def _bmcpinit(i, c = {}):
	return rwg(cc(), "", byte(cc(c, {"val": str(i)}, ["border"])), "Message Type")

def bmcp():
	return con(byte(cc({}, {"desc": "Message Type"})), varlen(cc({}, {"border": T|B|L|R, "desc": "Message Data \\\\ $N$ Bytes"})))

def bmcpconnectreq():
	return con(_bmcpinit(0), cryptoinitidlist({"border": T|B|L|R}))

def bmcpconnectrep():
	return con(_bmcpinit(1), cryptoinitid({"border": T|B|L|R}))

def bmcpdisconnect():
	return con(_bmcpinit(2, {"border": T|B|L|R}))

def bmcpkill():
	return con(_bmcpinit(3, {"border": T|B|L|R}))

def bmcpcryptoinit():
	return con(_bmcpinit(4), varlen(cc({}, {"desc": "Crypto Initialization Data \\\\ $N$ Bytes", "border": T|B|L|R})))

def bmcpack():
	return con(_bmcpinit(5), flexnum({"desc": "Ack Data ID", "border": T|B|L|R}))

def bmcpchprotoreq():
	return con(_bmcpinit(6), string({"desc": "\\gls{protoid}", "border": T|B|L|R}))

def bmcpchblockstatreq():
	return con(_bmcpinit(7), channelidlist({"border": T|B|L|R}))

def bmcpchblockstatrep():
	return con(_bmcpinit(8), channelreportlist({"flexnumstyle": "short", "border": T|B|L|R}))

def bmcpopenchreq():
	return con(_bmcpinit(9), channelid(), string({"desc": "\\gls{protoid}", "border": T|B|L|R}))

def bmcpthrottle():
	return con(_bmcpinit(10), flexnum({"desc": "Bytes Per Second", "border": T|B|L|R}))

###

def link():
	return con(dataid(), channelid(), data({"desc": "Channel Data", "border": T|B|L|R}))

###

def _keycinit(i, c = {}):
	return rwg(cc(), "", byte(cc(c, {"val": str(i)}, ["border"])), "Key Type")

def keyc():
	return con(byte(cc({}, {"desc": "Key Type"})), varlen(cc({}, {"border": T|B|L|R, "desc": "Key Data \\\\ $N$ Bytes"})))

def keycrsa():
	return con(_keycinit(0), bigint(cc({}, {"desc": "Modulus"})), bigint(cc({}, {"desc": "Exponent", "border": T|B|L|R})))

###

def _sblitinit(i, c = {}):
	return rwg(cc(), "", byte(cc(c, {"val": str(i)}, ["border"])), "Message Type")

def sblit():
	return con(byte(cc({}, {"desc": "Message Type"})), varlen(cc({}, {"border": T|B|L|R, "desc": "Message Data \\\\ $N$ Bytes"})))
	
def versionsverlauf(cc):
	return con(fixdata({"desc": "Versionsverlauf", "size":20, "border" : T|B|L|R}))

def geraete(cc):
	return con(fixdata({"desc": "Geräte mit der aktuellen Version", "size":20, "border" : T|B|L|R}))

def sblitauthreq():
	return con(_sblitinit(0), fixdata({"desc": "Zufallsdaten", "size": 64, "border" : T|B|L|R}))

def sblitauthres():
	return con(_sblitinit(1), fixdata({"desc": "Zufallsdaten", "size": 128, "border" : T|B|L|R}))

def sblitfilereq(c = {}):
	return con(_sblitinit(2), string({"desc": "Dateipfad", "border" : T|B|L|R, "varlensize" : 3}), array(cc(c, {"rwgid": "llalist", "name": "Version", "content": versionsverlauf(cc(c)), "border" : T|B|L|R}, ["border"])))#, array({"desc" : "Versionsverlauf"}))
	
def sblitfileres(c = {}):
	return con(_sblitinit(3),byte({"desc" : "Need-Flag"}), string({"desc": "Dateipfad", "border" : T|B|L|R, "varlensize" : 3}), array(cc(c, {"rwgid": "llalist", "name": "Version", "content": versionsverlauf(cc(c)), "border" : T|B|L|R}, ["border"])))
	
def sblitfilemsg(c = {}):
	return con(_sblitinit(4), data({"desc": "Dateiinhalt"}), string({"desc": "Dateipfad", "varlensize" : 3}),array(cc(c, {"rwgid": "llalist", "name": "Version", "content": versionsverlauf(cc(c)), "border" : T|B|L|R}, ["border"])), array(cc(c, {"rwgid": "llalist", "name": "Gerät", "content": geraete(cc(c)), "border" : T|B|L|R}, ["border"])))
	
def sblitfiledel():
	return con(_sblitinit(5), string({"desc": "Dateipfad", "varlensize" : 3, "border" : T|B|L|R}))
	
def sblitrefdev():
	return con(_sblitinit(6), byte({"desc" : "File-Flag"}), string({"desc": "Dateipfad", "varlensize" : 3, "border" : T|B|L|R}))
	
def sblitpartfilereq(c = {}):
	return con(_sblitinit(7), array(cc(c, {"rwgid": "llalist", "name": "Version", "border" : T|B|L|R, "content": versionsverlauf(cc(c))}, ["border"])))
	
def sblitpartfileres(c = {}):
	return con(_sblitinit(8), array(cc(c, {"rwgid": "llalist", "name": "Version", "content": versionsverlauf(cc(c)), "border" : T|B|L|R}, ["border"])), byte({"desc" : "Need-Flag", "border" : T|B|L|R}))

def sblitpartfilemsg(c = {}):
	return con(_sblitinit(9), array(cc(c, {"rwgid": "llalist", "name": "Version", "content": versionsverlauf(cc(c)), "border" : T|B|L|R}, ["border"])), data({"desc": "Dateiinhalt"}), string({"desc": "Dateipfad", "varlensize" : 3}), array(cc(c, {"rwgid": "llalist", "name": "Gerät", "content": geraete(cc(c)), "border" : T|B|L|R}, ["border"])))
	
def sblitpartfiledel():
	return con(_sblitinit(10), string({"desc": "Dateipfad", "varlensize" : 3, "border" : T|B|L|R}))

def sblitfiledelpart(c = {}):
	return con(_sblitinit(11), array(cc(c, {"rwgid": "llalist", "name": "Version", "border" : T|B|L|R, "content": versionsverlauf(cc(c))}, ["border"]))) 
	 
PROTOCOLS = {
	"isproto": {
		"latexname": "\\gls*{isproto}",
		"messages": {
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
			"icreq": "Integration Connect Request",
			"np": "Network Packet",
			"acsa": "Application Channel Slot Assign",
			"acd": "Application Channel Data"
		}
	},
	"asproto": {
		"latexname": "\\gls*{asproto}",
		"messages": {
			"revision": "Revision",
			"genkey": "Generate Key",
			"joinnet": "Join Network",
			"slotassign": "Slot Assign",
			"data": "Data",
			"addrpubkey": "Address Public Key",
			"joindefnets": "Join Default Networks",
			"keyenc": "Key Encrypt",
			"keydec": "Key Decrypt",
			"cryptoresponse": "Key Crypto Response",
			"appchoutreq": "Application Channel Outgoing Request",
			"appchinreq": "Application Channel Incoming Request",
			"appchaccept": "Application Channel Accept",
			"appchconnected": "Application Channel Connected",
			"appchdata": "Application Channel Data",
			"keyencblocksizereq": "Key Encryption Block Size Request",
			"keynum": "Key Number Response"
		}
	},
	"crisp": {
		"latexname": "\\acrshort*{crisp}",
		"messages": {
			"neighreq": "Neighbor Request"
		}
	},
	"bmcp": {
		"latexname": "\\acrshort*{bmcp}",
		"messages": {
			"connectreq": "Connect Request",
			"connectrep": "Connect Reply",
			"disconnect": "Disconnect",
			"kill": "Kill",
			"cryptoinit": "Crypto Init",
			"ack": "Ack",
			"chprotoreq": "Change Protocol Request",
			"chblockstatreq": "Channel Block Status Request",
			"chblockstatrep": "Channel Block Status Report",
			"openchreq": "Open Channel Request",
			"throttle": "Throttle"
		}
	},
	"link": {
		"latexname": "\\gls*{link}",
		"gentext": "\\gls*{link} Packet",
		"messages": {}
	},
	"keyc": {
		"latexname": "\\gls*{keyc}",
		"type": "\\comp",
		"gentext": "\\gls*{keyc} -- Genereller Componentaufbau",
		"messages": {
			"rsa": "RSA Key"
		}
	},
	"sblit" : {
		"latexname" : "\\gls*{sblit}", 
		"messages" : {
			"authreq" : "\\gls*{authreq}",
			"authres": "\\gls*{authres}", 
			"filereq" : "\\gls*{filereq}",
			"fileres" : "\\gls*{fileres}",
			"filemsg" : "\\gls*{filemsg}",
			"filedel" : "\\gls*{filedel}",
			"refdev" : "\\gls*{refdev}",
			"partfilereq" : "\\gls*{partfilereq}",
			"partfileres" : "\\gls*{partfileres}",
			"partfilemsg" : "\\gls*{partfilemsg}",
			"partfiledel" : "\\gls*{partfiledel}",
			"filedelpart" : "\\gls*{filedelpart}"
			# format ist immer: { ..., "messageid": "Voller Name der Message, wurscht ob mit glossary oder direkt", ... }
			# protocol key ist hier "sblit", messages sind "req" und "res" - d.h. es müssen folgende funktionen definiert sein: sblit, sblitauthreq, sblitauthres
		}
	}
}

if WRITEPROTOCOLS == True:
	WRITEPROTOCOLS = []
	for protocol in PROTOCOLS:
		WRITEPROTOCOLS.append(protocol)

sys.stderr.write("writing %s for protocols: %s\n" % ("headings" if HEADINGS else ("empty " if EMPTY else "") + "bytefields", ", ".join(WRITEPROTOCOLS)))

for protocol in WRITEPROTOCOLS:
	print("")
	info = PROTOCOLS[protocol]
	if HEADINGS:
		print(genheadings("dcl", protocol, info))
	else:
		print(gen("dcl", protocol, info))
	print("")