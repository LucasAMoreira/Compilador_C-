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
	'OBT', #abre colchetes
	'CBT', # fecha colchetes
	'ID',
	'NUM',
	'RELOP',
	'PLUS', # Operador aritmético
	'MINUS',
	'TIMES',
	'DIVIDE',
	'COMMENT',
	'ATTRIBUTION',
	'COMMA',
	'SEMICOLON',
	'OP',
	'CP',	
	'OBR',# abre chaves
	'CBR'	
]

# Tokens são a lista anterior e as palavras reservadas.
tokens =  tokens + list(reservadas.values())

# Expressões regulares que definem os tokens

digito = r'([0-9])'

t_NUM          = r'('+digito + r'+' + digito +r'*)'
t_ATTRIBUTION  = r'='
t_COMMA        = r','
t_SEMICOLON    = r';'

t_ignore  = ' \t'# Ignora tabulação 

abre = r'/\*'	
fecha = r'\*/'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_OBT =r'\['
t_CBT = r'\]'
t_OP = r'\('
t_CP = r'\)'
t_OBR = r'\{'
t_CBR = r'\}'	
	

"""	
def t_BRACKETS(t):
	r'\[ | \]'
	if(t.value=='['):
		t.value=['[','OBT']
	if(t.value==']'):
		t.value=[']','CBT']
	return t
"""

def t_ID(t):
	r'([a-zA-Z] + [a-zA-Z]*)'
	t.type = reservadas.get(t.value,'ID')
	return t
	
	
def t_RELOP(t):
	r'<= | >= | == | != | > | < '
	if(t.value=='<='):
		t.value=['<=','LE']
	if(t.value=='>='):
		t.value=['>=','GE']
	if(t.value=='=='):
		t.value=['==','EQ']
	if(t.value=='!='):
		t.value=['!=','NE']	
	if(t.value=='<'):
		t.value=['<','LT']
	if(t.value=='>'):
		t.value=['>','GT']
	return t

# DEVE estar antes de ARIOP
def t_COMMENT(t):	
	r'(/\*){1}([^{/*}] | \*[^/] | /[^\*])*(\*/){1}'
	pass

# def t_SUM(t):
# 	r'\+ | \-'
# 	if(t.value=='+'):
# 		t.value = ['+','PLUS']
# 	if(t.value=='-'):
# 		t.value = ['-','MINUS']	
# 	return t

# def t_MULT(t):
# 	r'\* | /'
# 	if(t.value=='*'):
# 		t.value = ['*','TIMES']
# 	if(t.value=='/'):
# 		t.value = ['/','DIVIDE']
# 	return t
	
"""	
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
		t.value=['(','OP']
	if(t.value==')'):
		t.value=[')','CP']
	return t

def t_BRACES(t):
	r'\{ | \}'
	if(t.value=='{'):
		t.value=['{','OBC']
	if(t.value=='}'):
		t.value=['}','CBC']
	return t
"""


# Regra para caracteres ilegais. A assinatura do método DEVE ser em letras minúsculas
def t_error(t):
	#("ERROR: caracter ilegal: "+ t.value[0]+ " in line "+str(t.lineno))
	t.value=t.value[0]	
	t.type='ERROR'
	t.lexer.skip(1)
	return t
	
# Regra que conta número de linhas
def t_numLinhas(t):
	r'\n+'
	t.lexer.lineno += len(t.value) 

lexer = lex.lex()











