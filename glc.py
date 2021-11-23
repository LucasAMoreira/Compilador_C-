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

def p_declaracao(p):
	'''
	declaracao : var_declaracao
			 | fun_declaracao
	'''

def p_var_declaracao(p):
	'''
	var_declaracao : tipo_especificador ID ';'	
				| tipo_especificador ID '[' NUM ']' ';'
	'''

def p_tipo_especificador(p):
	'''
	tipo_especificador : INT
				    | VOID
	'''

def p_fun_declaracao(p):
	'''
	fun_declaracao : tipo_especificador ID '(' params ')' composto_decl
	'''
	
def p_params(p):
	'''
	params : param_lista
		  | VOID
	'''

def p_param_lista(p):
	'''
	param_lista : param_lista ',' param
			  | param
	'''

def p_param(p):
	'''
	param : tipo_especificador ID 
		 | tipo_especificador ID '[' ']'
	'''

def p_composto_decl(p):
	'''
	composto_decl : '{' local_declaracao statement_lista '}'
	'''

def p_local_declaracoes(p):
	'''
	local_declaracoes : local_declaracoes var_declaracao
				   | vazio
	'''
	
def p_statement_lista(p):
	'''
	statement_lista : statement_lista statement
				 | vazio
	'''

def p_statement(p):
	'''
	statement : expressao_decl
			| composto decl 
			| selecao_decl 
			| iteracao_decl 
			| retorno_decl
	'''

def p_expressao_decl(p):
	'''
	expressao_decl : expressao ';'
				| ';'
	'''

def selecao_decl(p):
	'''
	selecao_decl : IF '(' expressao ')' statement
			   | IF '(' expressao ')' statement ELSE statement
	'''

def p_iteracao_decl(p):
	'''
	iteracao_decl : WHILE '(' expressao ')' statement
	'''

def p_retorno_decl(p):
	'''
	retorno_decl : RETURN ';'
			   | RETURN expressao ';'
	'''
	
def p_expressao(p):
	'''
	expressao : var '=' expressao
			| simples_expressao
	'''

def p_var(p):
	'''
	var : ID
	    | ID '[' expressao ']'
	'''

def p_simples_expressao(p):
	'''
	simples_expressao : soma_expressao relacional soma_expressao 
				   | soma_expressao
	'''

def p_relacional(p):
	'''
	relacional : RELOP
	'''
			
def p_soma_expressao(p):
	'''
	soma_expressao : soma_expressao soma termo
				| termo
	'''
	
def p_soma(p):
	'''
	soma : '+'
		| '-'
	'''
def p_termo(p):
	'''
	termo : termo mult fator
		 | fator
	'''
	
def p_mult(p):
	'''
	mult : '*'
		| '/'
	'''

def p_fator(p):
	'''
	fator : '(' expressao ')'
		 | var
		 | ativacao
		 | NUM
	'''

def p_ativacao(p):
	'''
	ativacao : ID '(' args ')'
	'''

def p_args(p):
	'''
	args : arg_lista 
		| lista
	'''
	
def p_arg_lista(p):
	'''
	arg_lista : arg_lista ',' expressao
			| expressao
	'''


# O TRECHO ABAIXO ESTÁ NA DOCUMENTAÇÃO DO PLY
# ESTAMOS USANDO APENAS PARA TESTES


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


