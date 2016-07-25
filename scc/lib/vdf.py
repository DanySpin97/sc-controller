#!/usr/bin/env python2
"""
VDF file reader.
"""
import shlex

def parse_vdf(fileobj):
	"""
	Converts VDF file or file-like object into python dict
	
	Throws ValueError if profile cannot be parsed.
	"""
	rv = {}
	stack = [ rv ]
	lexer = shlex.shlex(fileobj)
	key = None
	
	t = lexer.get_token()
	while t:
		if t == "{":
			# Set value to dict and add it on top of stack
			if key is None:
				raise ValueError("Dict without key")
			value = {}
			stack[-1][key] = value
			stack.append(value)
			key = None
		elif t == "}":
			# Pop last dict from stack
			stack = stack[0:-1]
		elif key is None:
			key = t.strip('"')
		else:
			stack[-1][key] = t.strip('"')
			key = None
		
		t = lexer.get_token()
	
	if len(stack) > 1:
		raise ValueError("Unfinished dict")
	
	return rv

if __name__ == "__main__":
	print parse_vdf(file('app_generic.vdf', "r"))

