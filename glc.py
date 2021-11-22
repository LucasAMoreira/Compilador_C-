import ply.yacc as yacc
from regex import tokens


# ATENÇÃO: ':' É SEPARADO POR ESPAÇO!

def p_programa(p):
	'programa : declaracao_lista'

def p_declaracao_lista(p):
	'''
	declaracao_lista : declaracao_lista 
				  | declaracao
	'''

''' 
# Error rule for syntax errors
def p_error(p):
	print("Syntax error in input!")
 
# Build the parser
parser = yacc.yacc()
 
while True:
	try:
		s = raw_input('calc > ')
	except EOFError:
		break
	if not s: continue
	result = parser.parse(s)
	print(result)
'''

