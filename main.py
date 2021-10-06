import regex
import ply.lex as lex

# Cria lexer com base nas expressões regulares do arquivo regex.py
lexer = lex.lex(module=regex, optimize =1);

# Abre arquivo e armazena seu conteúdo na variável 'programa'
arq = open('./Testes/sort.c-','r')
programa = arq.read();

# Lexer recebe programa como entrada
lexer.input(programa)
 
# Enquanto houver conteúdo, lê e tokeniza
i=0
while True:
	tok = lexer.token()
	if not tok: 
		break     
	print(tok.value, tok.type, tok.lineno)
	i=i+1

print('Número de tokens: '+str(i))
arq.close();

