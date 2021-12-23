import ply.yacc as yacc
import ply.lex as lex
import regex
import glc
import astree
from AST import *
import sys

def build_tree(tokens):
	if tokens:
		if type(tokens) == str:
			root = astree.TreeNode(tokens)
			return root
		root = astree.TreeNode(tokens[0])
		for token in tokens[1:]:
			root.add_child(build_tree(token))
		return root
	return None
	
# Cria lexer com base nas expressões regulares do arquivo regex.py
# NÃO ativamos o modo 'optmize', pois com ele não podemos identificar qual é a linha
lexer = regex.lexer

# Caso não haja programa de entrada avisa o usuário
if(len(sys.argv)==1):
	print('ERROR: Arquivo de entrada não especificado!')
	
else:
	# Nome do arquivo de entrada do lexer
	parametro = sys.argv[1]

	# Abre arquivo e armazena seu conteúdo na variável 'programa'
	arq = open(parametro,'r')
	programa = arq.read();
	
	# Lexer recebe programa como entrada
	lexer.input(programa)

	# Cria parser com as expressões regulares de glc
	parser = glc.parser

	try:
		teste = parser.parse(programa, lexer=lexer)
		tree = build_tree(teste)
		#tree.print_tree()
		#print("######################")
		tree = substitute(tree)
		tree.print_tree()
		decl = retornaOp(tree)
		#print(decl)
		decl = retornaSep(decl)
		decl = inverte(decl)
		decl = divide(decl)
		decl = separa(decl)
		decl = padding(decl)
		print(decl)
		
	except EOFError:
		print("EOF")
		pass
	arq.close();


