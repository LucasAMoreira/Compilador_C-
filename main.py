import ply.yacc as yacc
import ply.lex as lex
import regex
import glc
import astree
from traducao import *
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

	# Cria arquivo onde será armazenado código MIPS
	output = '\nj main\n \noutput:\nmove $a0, $v0\nli $v0, 1\nsyscall\njr $ra\n'
	arquivo = open("codigo.asm","w")
	arquivo.write("# ACH2087 - 2021\n# Código MIPS\n# GitHub: LucasAMoreira/Compilador_C-\n"+output)



	arquivo.close()

	try:
		teste = parser.parse(programa, lexer=lexer)
		tree = build_tree(teste)
		tree.print_tree()
		print("######################")
		#tree = substitute(tree)
		#tree = simple_ast(tree)
		tree.print_tree()
		tree = t_traduz(tree)

		#decl = retornaOp(tree)
		#print(decl)
		'''
		decl = retornaSep(decl)
		decl = inverte(decl)
		decl = divide(decl)
		decl = separa(decl)
		decl = padding(decl)
		decl = ordena(decl)
		decl = simplifica(decl)
		decl = addTemp(decl)
		'''
		#geraCod(decl)
		#for d in decl:
		#	d = " ".join(d)
		#	print(d, end=";\n")


		#print(decl)

	except EOFError:
		print("EOF")
		pass
	arq.close();
