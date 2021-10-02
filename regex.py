import ply.lex as lex

# module: regex.py
# This module just contains the lexing rules


# Palavras reservadas
reservadas = {
	'else' : 'ELSE',
	'if' : 'IF',
	'int' : 'INT',
	'return' : 'RETURN',
	'void' : 'VOID',
	'while' : 'WHILE'
}

# Lista de tokens
tokens=[
	'ID',
	'NUM',
	'RELOP',
	'ARIOP', # Operador aritmético
	'COMENT',
	'ATRIBUITION',
	'COLON',
	'SEMICOLON',
	'PARENTHESIS'
	'COLCHETES',
	'CHAVE',
	
];

# Tokens são a lista anterior e as palavras reservadas.
tokens =  tokens + list(reservadas.values())


# Expressões regulares que definem os tokens

digito = r'([0-9])'
letra = r'([a-zA-Z])'

t_NUM          = r'('+digito + r'+' + digito +r'*)'
t_RELOP        = r'< | <= | > | >= | == | !='
t_ARIOP        = r'\+ | \- | \* | /'

#t_COMENT

t_ATRIBUITION  = r'='
t_COLON        = r','
t_SEMICOLON    = r';'

'''  
t_PARENTHESIS  = r'(\()'
t_COLCHETES = r'\[ | \]'
t_CHAVE = r'\{ | \}'
'''

def t_ID(t):
	r'([a-zA-Z] + [a-zA-Z]*)'
	t.type = reservadas.get(t.value,'ID')
	return t;



######################################################################################
#				TESTES
######################################################################################

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)


lexer = lex.lex();

# Test it out
data =  'var=5; /*COMENTÁRIO*/ \nif(var>5)\n\tvar = var + 1;'

print(data)
 # Give the lexer some input
lexer.input(data)
 
 # Tokenize
while True:
     tok = lexer.token()
     if not tok: 
         break      # No more input
     print(tok)



















