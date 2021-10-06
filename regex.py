import ply.lex as lex

# modulo: regex.py
# Este módulo contêm as expressões regulares do lexer

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
	'BRACKETS', #colchetes
	'ID',
	'NUM',
	'RELOP',
	'ARIOP', # Operador aritmético
	'COMMENT',
	'ATTRIBUTION',
	'COMMA',
	'SEMICOLON',
	'PARENTHESES',	
	'BRACES',# chave	
];

# Tokens são a lista anterior e as palavras reservadas.
tokens =  tokens + list(reservadas.values())


# Expressões regulares que definem os tokens

digito = r'([0-9])'

t_NUM          = r'('+digito + r'+' + digito +r'*)'
t_ATTRIBUTION  = r'='
t_COMMA        = r','
t_SEMICOLON    = r';'

t_ignore  = ' \t '# Ignora tabulação 

abre = r'/\*'	
fecha = r'\*/'

	
def t_BRACKETS(t):
	r'\[ | \]'
	if(t.value=='['):
		t.value=['BRACKETS','OBT']
	if(t.value==']'):
		t.value=['BRACKETS','CBT']
	return t


def t_ID(t):
	r'([a-zA-Z] + [a-zA-Z]*)'
	t.type = reservadas.get(t.value,'ID')
	return t;

def t_COMMENT(t):
	r'/\* ([^(abre)] | [^(*/)])* \*/'
	pass
	
	
def t_RELOP(t):
	r'< | <= | > | >= | == | !='
	if(t.value=='>'):
		t.value=['>','GT']
	if(t.value=='>='):
		t.value=['>=','GE']
	if(t.value=='<'):
		t.value=['<','LT']
	if(t.value=='<='):
		t.value=['<=','LE']
	if(t.value=='=='):
		t.value=['==','EQ']
	if(t.value=='!='):
		t.value=['!=','NE']	
	return t
	
def t_ARIOP(t):
	r'\+ | \- | \* | /'
	if(t.value=='+'):
		t.value = ['+','PLUS']
	if(t.value=='-'):
		t.value = ['-','MINUS']
	if(t.value=='*'):
		t.value = ['*','TIMES']
	if(t.value=='/'):
		t.value = ['/','DIVIDE']
	return t


def t_PARENTHESES(t):
	r'\( | \)'
	if(t.value=='('):
		t.value=['PARENTHESES','OP']
	if(t.value==')'):
		t.value=['PARENTHESES','CP']
	return t

def t_BRACES(t):
	r'\{ | \}'
	if(t.value=='{'):
		t.value=['BRACES','OBC']
	if(t.value=='}'):
		t.value=['BRACES','CBC']
	return t

# Regra para caracteres ilegais. A assinatura do método DEVE ser em letras minúsculas
def t_error(t):
	print("ERROR: caracter ilegal: "+ t.value[0]+ " in line "+str(t.lineno))
	t.lexer.skip(1)

# Regra que conta número de linhas
def t_numLinhas(t):
	r'\n+'
	t.lexer.lineno += len(t.value) 














