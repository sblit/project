
L = int("1000", 2)
R = int("0100", 2)
T = int("0010", 2)
B = int("0001", 2)

"""
COMPONENTS = {}

PERMITRIGHTWORDGROUP = True

def _borderstr(border):
	return ("l" if (border & L) else "")\
		 + ("r" if (border & R) else "")\
		 + ("t" if (border & T) else "")\
		 + ("b" if (border & B) else "")

def surroundRightWordGroup(content, text):
	return "\\begin{rightwordgroup}{"+text+"}\n"\
		 + content + "\n"\
		 + "\\end{rightwordgroup}"

def draw(what, border):
	args = what["args"] if what.has_key("args") else {}
	msg = COMPONENTS[what["msg"]]
	
	if msg.has_key("args"):
		for k, v in msg["args"].iteritems():
			if not args.has_key(k):
				args[k] = v
	
	children = msg["children"] if msg.has_key("children") else []
	
	content = msg["draw"](args, children, border)
	
	if what.has_key("rightwordgroup") and (PERMITRIGHTWORDGROUP == True or PERMITRIGHTWORDGROUP.count(what["msg"]) > 0):
		content = surroundRightWordGroup(content, what["rightwordgroup"])
	
	return content

def drawByte(args, children, border):
	content = ""
	if args.has_key("val"):
		content += "\\code{"+args["val"]+"}"
	if args.has_key("desc"):
		content += args["desc"]
	return "\\wordbox["+_borderstr(border)+"]{1}{"+content+"}"

def drawFlexNum(args, children, border):
	return "\\wordbox["+_borderstr(border&(L|R|T))+"]{2}{"+args["desc"]+" \\\\ \\flexnumfield} \\\\ \n"\
		 + "\\skippedwords \\\\ \n"\
		 + "\\wordbox["+_borderstr(border&(L|R|B))+"]{1}{}"

def drawVarLen(args, children, border):
	return "\\wordbox["+_borderstr(border&(L|R|T))+"]{2}{"+args["desc"]+"} \\\\ \n"\
		 + "\\skippedwords \\\\ \n"\
		 + "\\wordbox["+_borderstr(border&(L|R|B))+"]{1}{}"

def drawGeneral(args, children, border):
	return " \\\\ \n".join([draw(child, border) for child in children])

def beginBytefield(wordsize):
	return "\\begin{figure}[tbh]"\
		 + "\\begin{centering}"\
		 + "\\begin{bytefield}[bitwidth="+("%.1f" % (24.0 / wordsize))+"em]{"+str(wordsize)+"}"\
		 + " \\\\ "\
		 + "\\bitheader{0-"+str(wordsize-1)+"}"\
		 + " \\\\ "

def endBytefield(title):
	return "\\end{bytefield}"\
		 + "\\par\\end{centering}"\
		 + "\\protect\\caption{"+title+"}"\
		 + "\\end{figure}"

def drawInterserviceMessage(args):
	return beginBytefield(8)\
		 + draw({ "msg": "byte",  "args": { "val": args["type"] }, "rightwordgroup": "\\isprotomsgtype" }, T|L|R)\
		 + " \\\\ "\
		 + (drawInterserviceMessageData(args["children"], args["permitrightwordgroup"] if args.has_key("permitrightwordgroup") else True) if args.has_key("children") else "")\
		 + endBytefield("\\gls*{isproto} -- " + args["name"] + "-Message")

def drawInterserviceGeneralMessage(args):
	return beginBytefield(8)\
		 + (" \\\\ \n".join([draw(child, T|L|R) for child in args["children"][:-1]] + [draw(args["children"][-1], T|B|L|R)]) if args.has_key("children") else "")\
		 + endBytefield("\\gls*{isproto} -- Genereller Messageaufbau")

def drawInterserviceMessageData(children, permitrightwordgroup):
	global PERMITRIGHTWORDGROUP
	old = PERMITRIGHTWORDGROUP
	PERMITRIGHTWORDGROUP = permitrightwordgroup
	content = " \\\\ \n".join([draw(child, T|L|R) for child in children[:-1]])
	content += draw(children[-1], T|B|L|R)
	if permitrightwordgroup == True:
		content = surroundRightWordGroup(content, "\\isprotomsgdata")
	PERMITRIGHTWORDGROUP = old
	return content

COMPONENTS = {
	
	"byte": {
		"draw": drawByte
	},
	"flexnum": {
		"draw": drawFlexNum
	},
	
	"varlen": {
		"draw": drawVarLen
	},
	
	"llalist": {
		"draw": drawGeneral,
		"children": [
			{ "msg": "flexnum", "args": { "desc": "LLA Count" } },
			{ "msg": "lla", "rightwordgroup": "LLA" },
			{ "msg": "varlen", "args": { "desc": "$\\cdots$" }, "rightwordgroup": "LLA" }
		]
	},
	"lla": {
		"draw": drawGeneral,
		"children": [
			{ "msg": "byte", "args": { "desc": "LLA Type" } },
			{ "msg": "varlen", "args": { "desc": "LLA Data" } }
		]
	},
	
	"key": {
		"draw": drawGeneral,
		"children": [
			{ "msg": "byte", "args": { "desc": "Key Type" } },
			{ "msg": "varlen", "args": { "desc": "Key Data \\\\ $N$ Bytes" } }
		]
	}
	
}

ISGENERAL = {
	"isgeneral": {
		"name": "\\isprotogeneral",
		"children": [
			{ "msg": "flexnum", "args": { "desc": "\\isprotomsgtype" } },
			{ "msg": "varlen", "args": { "desc": "\\isprotomsgdata \\\\ $N$ Bytes" } }
		]
	}
}

ISMSG = {
	
	"isprotoversion": {
		"type": "0",
		"name": "\\isprotoversion",
		"children": [
			{ "msg": "flexnum", "args": { "desc": "Version ID" } }
		]
	},
	"isprotollareq": {
		"type": "1",
		"name": "\\isprotollareq",
		"children": [
			{ "msg": "flexnum", "args": { "desc": "Limit" } }
		]
	},
	"isprotollarep": {
		"type": "2",
		"name": "\\isprotollarep",
		"children": [
			{ "msg": "llalist" }
		],
		"permitrightwordgroup": [ "lla", "varlen" ]
	},
	"isprotots": {
		"type": "3",
		"name": "\\isprotots",
		"children": [
			{ "msg": "flexnum", "args": { "desc": "Address Slot" } },
			{ "msg": "key", "rightwordgroup": "Address Key" }
		],
		"permitrightwordgroup": [ "byte", "varlen" ]
	}
	
}
"""
#print(draw({ "msg": "flexnum", "args": {"desc": "Version ID"}, "rightwordgroup": "\\isprotomsgdata" }, T|L|R|B))
#print(drawInterserviceMessage(ISMSG["is-version"]))
#print(drawInterserviceMessage(ISMSG["is-llareq"]))
"""
def createCommands(msgdict, drawFunction):
	for msgid, msg in msgdict.iteritems():
		print("\\newcommand{\\"+msgid+"bytefield}{"+drawFunction(msg)+"}")
		print("")

createCommands(ISGENERAL, drawInterserviceGeneralMessage)
createCommands(ISMSG, drawInterserviceMessage)
"""
"""
\begin{figure}[tbh]
\begin{centering}

\begin{bytefield}[bitwidth=3em]{8}
	\\
	\bitheader{0-7} \\
	
	\begin{rightwordgroup}{\isprotomsgtype}
		\wordbox[tlr]{1}{\code{0}}
	\end{rightwordgroup} \\
	
	\begin{rightwordgroup}{\isprotomsgdata}
		\wordbox[tlr]{2}{Version ID \\ \flexnumfield} \\
		\skippedwords \\
		\wordbox[blr]{1}{}
	\end{rightwordgroup}
	
\end{bytefield}

\par\end{centering}
\protect\caption{\gls*{isproto} -- \isprotoversion-Message}
\end{figure}
"""

""""isprotollareq": {
		"type": "1",
		"name": "\\isprotollareq",
		"children": [
			{ "msg": "flexnum", "args": { "desc": "Limit" } }
		]
	},
	"isprotollarep": {
		"type": "2",
		"name": "\\isprotollarep",
		"children": [
			{ "msg": "llalist" }
		],
		"permitrightwordgroup": [ "lla", "varlen" ]
	},
	"isprotots": {
		"type": "3",
		"name": "\\isprotots",
		"children": [
			{ "msg": "flexnum", "args": { "desc": "Address Slot" } },
			{ "msg": "key", "rightwordgroup": "Address Key" }
		],
		"permitrightwordgroup": [ "byte", "varlen" ]
	}"""

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
	if c.has_key("val"):
		content += "\\code{"+c["val"]+"}"
	if c.has_key("desc"):
		content += c["desc"]
	return "\\wordbox["+_borderstr(c["border"])+"]{1}{"+content+"}\n"

###

def byte(c):
	return fixlen(cc(c, {}, ["val", "desc"]))

def flexnum(c):
	return varlen(cc(c, {"desc": c["desc"] + " \\\\ \\flexnumfield"}, ["border"]))

def lla(c):
	return con(flexnum(cc(c, {"desc": "LLA Type"})), varlen(cc(c, {"desc": "LLA Data"}, ["border"])))

def llalist(c):
	return con(rwg(c, "llalist", lla(cc(c)), "LLA"), rwg(c, "llalist", varlen(cc(c, {"desc": "$\\cdots$"}, ["border"])), "LLA"))

def key(c):
	return con(byte(cc(c, {"desc": "Key Type"})), varlen(cc(c, {"desc": "Key Data"}, ["border"])))

def data(c):
	return con(flexnum(cc(c, {"desc": "Data Length"})), varlen(cc(c, {"desc": "Data"}, ["border"])))

###

def _isinit(i):
	return rwg(cc(), "", byte(cc({}, {"val": str(i)})), "Message Type")

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

###

FUNCS = ["isprotoversion", "isprotollareq", "isprotollarep", "isprotots", "isprotoccreq"]

for func in FUNCS:
	print("\\newcommand{\\"+func+"bytefield}{"+bf(8, eval(func)(), "\\gls*{isproto} -- \\"+func+"-Message")+"}")
	print("")




