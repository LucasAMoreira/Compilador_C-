import regex
import ply.lex as lex


# Cria lexer com base nas expressões regulares do arquivo regex.py
# NÃO ativamos o modo 'optmize', pois com ele não podemos identificar qual é a linha
lexer = lex.lex(module=regex);

# Abre arquivo e armazena seu conteúdo na variável 'programa'
arq = open('./Testes/gcd.c-','r')
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

