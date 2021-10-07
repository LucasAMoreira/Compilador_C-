import regex
import ply.lex as lex
import sys

# Cria lexer com base nas expressões regulares do arquivo regex.py
# NÃO ativamos o modo 'optmize', pois com ele não podemos identificar qual é a linha
lexer = lex.lex(module=regex);

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
	 
	# Enquanto houver conteúdo, lê e tokeniza
	i=0
	while True:
		tok = lexer.token()
		if not tok: 
			break     
		print(tok)
		i=i+1

	print('Número de tokens: '+str(i))
	arq.close();



