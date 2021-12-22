import ply.yacc as yacc
import ply.lex as lex
import regex
import glc
from AST import *
import sys


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
		print(teste)
		#teste = ('raiz',('filho',('neto1','neto2','neto3')))
		#teste2=('irmao1','irmao2')
		#ast = criaAST(teste)
		#printAST(ast)
		arg1 = []
		arg2 = []
		op = []
		result = []
		percorre(teste,op,arg1,arg2)
		#quadPreLoad(op,arg1,arg2,result)
		#quadSoma(op,arg1,arg2,result)
		print(op)
		print(arg1)
		print(arg2)
		print(result)
		
	except EOFError:
		print("EOF")
		pass
	arq.close();


