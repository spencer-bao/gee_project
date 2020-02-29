#! /usr/bin/python3
#Author:        Gavin 931000651
#Date Created:  2/20/2020

import re, sys, string

debug = False
dict = { }
tokens = [ ]

class Statement( object ):
	def __str__(self):
		return ""

class WhileStatement( Statement ):
	def __init__(self, expr, block):
		self.expr = expr
		self.block = block
	
	def __str__(self):
		return "while" + str(self.expr) + str(self.block)

class IfStatement( Statement ):
	def __init__(self, expr, if_block, else_block):
		self.expr = expr
		self.if_block = if_block
		self.else_block = else_block

	def __str__(self):
		return "if" + str(if_block) + "else" + str(else_block)

class ElseStatement( Statement ):
	def __init__(self, identifier, expr):
		self.identifier = identifier
		self.expr = expr

#  Expression class and its subclasses
class Expression( object ):
	def __str__(self):
		return "" 
	
class BinaryExpr( Expression ):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right
		
	def __str__(self):
		return str(self.op) + " " + str(self.left) + " " + str(self.right)

class Number( Expression ):
	def __init__(self, value):
		self.value = value
		
	def __str__(self):
		return str(self.value)

##### BUILD CLASSES #####

class String( Expression ):
	def __init__(self, string):
		self.string = string
		
	def __str__(self):
		return str(self.string)
    
class VarRef( Expression ):
	def __init__(self, identifier):
		self.identifier = identifier
		
	def __str__(self):
		return str(self.identifier)

###########################

def error( msg ):
	#print msg
	sys.exit(msg)

# The "parse" function. This builds a list of tokens from the input string,
# and then hands it to a recursive descent parser for the PAL grammar.

def match(matchtok):
	tok = tokens.peek( )
	if (tok != matchtok): error("Expecting "+ matchtok)
	tokens.next( )
	return tok
	
##### ADD LOGIC #####

def factor( ):
	""" factor     = number | string | ident |  "(" expression ")" """

	tok = tokens.peek( )
	if debug: print ("Factor: ", tok)

	if re.match(Lexer.number, tok): #re.match(pattern, string) - if zero or more characters at the beginning of the string matches the pattern
		expr = Number(tok)
		tokens.next( )
		return expr

	if re.match(Lexer.string, tok):
		expr = String(tok)
		tokens.next( )
		return expr

	if re.match(Lexer.identifier, tok):
		expr = VarRef(tok)
		tokens.next( )
		return expr

	if tok == "(":
		tokens.next( )  # or match( tok )
		expr = expression( )
		tokens.peek( )
		tok = match(")")
		return expr

	error("Invalid operand")
	return

########################

def term( ):
	""" term    = factor { ('*' | '/') factor } """

	tok = tokens.peek( )
	if debug: print ("Term: ", tok)
	left = factor( )
	tok = tokens.peek( )
	while tok == "*" or tok == "/":
		tokens.next()
		right = factor( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left

def addExpr( ):
    # Note currently addExpr is in both factor and parse
	""" addExpr    = term { ('+' | '-') term } """

	tok = tokens.peek( )
	if debug: print ("addExpr: ", tok)
	left = term( )
	tok = tokens.peek( )
	while tok == "+" or tok == "-":
		tokens.next()
		right = term( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left

##### BUILD PARSE ROUTINES #####

def relationalExpr( ):
	""" relationalExpr = addExpr [ relation addExpr ] """
	""" relation    = "==" | "!=" | "<" | "<=" | ">" | ">=" """

	tok = tokens.peek( )
	if debug: print ("relationalExpr: ", tok)
	left = addExpr( )
	tok = tokens.peek( )
	while tok == "==" or tok == "!=" or tok == "<" or tok == "<=" or tok == ">" or tok == ">=":
		tokens.next()
		right = addExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left

def andExpr( ):
	""" andExpr    = relationalExpr { "and" relationalExpr } """

	tok = tokens.peek( )
	if debug: print ("andExpr: ", tok)
	left = relationalExpr( )
	tok = tokens.peek( )
	while tok == "and":
		tokens.next()
		right = relationalExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left

def expression( ):
	""" expression = andExpr { "or" andExpr } """

	tok = tokens.peek( )
	if debug: print ("expression: ", tok)
	left = andExpr( )
	tok = tokens.peek( )
	while tok == "or":
		tokens.next()
		right = andExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left

################################

##### BUILD PARSE ROUTINES #####

def parseStmtList( tokens ):
    # create a list of statements, put into a subclass of Statement, return an object containing the list
	""" gee = { Statement } """
	print (tokens)
	stmtList = []
	tok = tokens.peek( )
	while tok is not None:
		print (tok + '  PLEASE HELP')
			# need to store each statement in a list
		stmtList.append(parseStatement(tok))
		tok = tokens.next()
	return stmtList

def parseStatement(token): # classifies the token as a subclass of statement.
	""" statement = parseIfStatement |  parseWhileStatement  |  parseAssign """
	if token == ';':
		print ('YES')
		token = tokens.next()
		print (token + '   FU')
	if token == "if":
		print ('YES')
		return parseIfStatement()
	elif token == "while":
		return parseWhileStatement()
	#elif re.match(Lexer.identifier, token):
	#	return assign()
	else:
		#error("Invalid statement")
		return parseAssign()

def parseIfStatement():
	""" ifStatement = "if" expression block   [ "else" block ] """

	tok = tokens.peek()
	if debug: print("ifstatement: ", tok)
	if tok == "if":
		tokens.next()
		expres = expression()
		tokens.next()
		if_block = block()
		tok = tokens.next()
	if tok == "else":
		else_block = block()
	else:
		else_block = ''
	return IfStatement(expres, if_block, else_block)


def parseWhileStatement(  ):
	""" whileStatement = "while"  expression  block """

	tok = tokens.peek()
	if debug: print("whilestatement: ", tok)
	if tok == "while":
		tokens.next()
		expres = expression()
		tokens.next()
		block = block()
		tok = tokens.next()
	return WhileStatement(expres, block)


def parseAssign(  ):
	""" assign = ident "=" expression  eoln """
	tok = tokens.peek()
	if debug: print("assign: ", tok)
	
	while tok == '@' or tok == '~':
		tok = tokens.next
	starter = tok
	tok = tokens.next()
	if tok == "=":
		tok = tokens.next()
		expres = expression()
		tok = tokens.next()
		#print ('= ' + starter + ' ' + str(expres))
		return String("= " + starter + ' ' + str(expres))


def block(  ):
	""" block = ":" eoln indent stmtList undent """
	tok = tokens.peek( )
	if debug: print ("block: ", tok)

	if tok == ":":
		tok = tokens.next()
		if tok == ";":
			tok = tokens.next()
			if tok == "@":
				tok = tokens.next()
				stmtList = parseStmtList()
				tok = tokens.next()
				if tok == "~":
					return String(":;@" + str(stmtList) + "~")

################################

def parse( text ) :
	global tokens
	tokens = Lexer( text )
	# expr = addExpr( )
	# print (str(expr))
	stmtlist = parseStmtList( tokens )
	print (str(stmtlist))
	return


# Lexer, a private class that represents lists of tokens from a Gee
# statement. This class provides the following to its clients:
#
#   o A constructor that takes a string representing a statement
#       as its only parameter, and that initializes a sequence with
#       the tokens from that string.
#
#   o peek, a parameterless message that returns the next token
#       from a token sequence. This returns the token as a string.
#       If there are no more tokens in the sequence, this message
#       returns None.
#
#   o removeToken, a parameterless message that removes the next
#       token from a token sequence.
#
#   o __str__, a parameterless message that returns a string representation
#       of a token sequence, so that token sequences can print nicely

class Lexer :
	
	# The constructor with some regular expressions that define Gee's lexical rules.
	# The constructor uses these expressions to split the input expression into
	# a list of substrings that match Gee tokens, and saves that list to be
	# doled out in response to future "peek" messages. The position in the
	# list at which to dole next is also saved for "nextToken" to use.
	
	special = r"\(|\)|\[|\]|,|:|;|@|~|;|\$"
	relational = "<=?|>=?|==?|!="
	arithmetic = "\+|\-|\*|/"
	#char = r"'."
	string = r"'[^']*'" + "|" + r'"[^"]*"'
	number = r"\-?\d+(?:\.\d+)?"
	literal = string + "|" + number
	#idStart = r"a-zA-Z"
	#idChar = idStart + r"0-9"
	#identifier = "[" + idStart + "][" + idChar + "]*"
	identifier = "[a-zA-Z]\w*"
	lexRules = literal + "|" + special + "|" + relational + "|" + arithmetic + "|" + identifier
	
	def __init__( self, text ) :
		self.tokens = re.findall( Lexer.lexRules, text ) #re.findall(pattern, string) - returns all non-overlapping matches
		self.position = 0
		self.indent = [ 0 ]
	

	# The peek method. This just returns the token at the current position in the
	# list, or None if the current position is past the end of the list.
	
	def peek( self ) :
		if self.position < len(self.tokens) :
			return self.tokens[ self.position ]
		else :
			return None
	
	
	# The removeToken method. All this has to do is increment the token sequence's
	# position counter.
	
	def next( self ) :
		self.position = self.position + 1
		return self.peek( )
	
	
	# An "__str__" method, so that token sequences print in a useful form.
	
	def __str__( self ) :
		return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"



def chkIndent(line):
	ct = 0
	for ch in line:
		if ch != " ": return ct
		ct += 1
	return ct
		

def delComment(line):
	pos = line.find("#")
	if pos > -1:
		line = line[0:pos]
		line = line.rstrip()
	return line

def mklines(filename):
	inn = open(filename, "r")
	lines = [ ]
	pos = [0]
	ct = 0
	for line in inn:
		ct += 1
		line = line.rstrip( )+";"
		line = delComment(line)
		if len(line) == 0 or line == ";": continue
		indent = chkIndent(line)
		line = line.lstrip( )
		if indent > pos[-1]:
			pos.append(indent)
			line = '@' + line
		elif indent < pos[-1]:
			while indent < pos[-1]:
				del(pos[-1])
				line = '~' + line
		print (ct, "\t", line)
		lines.append(line)
	# print len(pos)
	undent = ""
	for i in pos[1:]:
		undent += "~"
	lines.append(undent)
	# print undent
	return lines



def main():
	"""main program for testing"""
	global debug
	ct = 0
	for opt in sys.argv[1:]:
		if opt[0] != "-": break
		ct = ct + 1
		if opt == "-d": debug = True
	if len(sys.argv) < 2+ct:
		print ("Usage:  %s filename" % sys.argv[0])
		return
	parse("".join(mklines(sys.argv[1+ct])))
	return


main()