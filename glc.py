import ply.yacc as yacc
import ply.lex as lex
# from regex import tokens
import regex

import warnings

def p_programa(p):
	'programa : declaracao_lista'
	p[0] = p[1]
	
 
def p_declaracao_lista(p):
	'''
	declaracao_lista : declaracao_lista declaracao
				| declaracao
	'''
	if len(p) == 3:
		p[0] = p[1] + p[2]
	else:
		p[0] = p[1]
 
def p_declaracao(p):
	'''
	declaracao : var_declaracao
			| fun_declaracao
	'''
	p[0] = p[1]
 
def p_var_declaracao(p):
	'''
	var_declaracao : tipo_especificador ID SEMICOLON	
		| tipo_especificador ID BRACKETS NUM BRACKETS SEMICOLON
	'''
	if len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
  
def p_tipo_especificador(p):
	'''
	tipo_especificador : INT
				    | VOID
	'''
	p[0] = p[1]
  
def p_fun_declaracao(p):
	'''
	fun_declaracao : tipo_especificador ID PARENTHESES params PARENTHESES composto_decl
	'''
	p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
 
def p_params(p):
	'''
	params : param_lista
		  | VOID
	'''
	p[0] = p[1]

def p_param_lista(p):
	'''
	param_lista : param_lista COMMA param
			  | param
	'''
	if len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1]
 
def p_param(p):
	'''
	param : tipo_especificador ID 
		 | tipo_especificador ID BRACKETS BRACKETS
	'''
	if len(p) == 3:
		p[0] = p[1] + p[2]
	else:
		p[0] = p[1] + p[2] + p[3] + p[4]
  
def p_composto_decl(p):
	'''
	composto_decl : BRACES local_declaracoes statement_lista BRACES
	'''
	p[0] = p[1] + p[2] + p[3] + p[4]
	
def p_local_declaracoes(p):
	'''
	local_declaracoes : local_declaracoes var_declaracao
				   | vazio
	'''
	if len(p) == 3 and p[1] and p[2]:
		p[0] = p[1] + p[2]
	else:
		p[0] = p[1]
  
def p_statement_lista(p):
	'''
	statement_lista : statement_lista statement
				 | vazio
	'''
	if len(p) == 3:
		p[0] = p[1] + p[2]
	else:
		p[0] = p[1]
  
def p_statement(p):
	'''
	statement : expressao_decl
			| composto_decl 
			| selecao_decl 
			| iteracao_decl 
			| retorno_decl
	'''
	p[0] = p[1]
 
def p_expressao_decl(p):
	'''
	expressao_decl : expressao SEMICOLON
				| SEMICOLON
	'''
	if len(p) == 3:
		p[0] = p[1] + p[2]
	else:
		p[0] = p[1]
  
def p_selecao_decl(p):
	'''
	selecao_decl : IF PARENTHESES expressao PARENTHESES statement
			   | IF PARENTHESES expressao PARENTHESES statement ELSE statement
	'''
	if len(p) == 6:
		p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
	else:
		p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]

def p_iteracao_decl(p):
	'''
	iteracao_decl : WHILE PARENTHESES expressao PARENTHESES statement
	'''
	p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
 
def p_retorno_decl(p):
	'''
	retorno_decl : RETURN SEMICOLON
			   | RETURN expressao SEMICOLON
	'''
	if len(p) == 3:
		p[0] = p[1] + p[2]
	else:
		p[0] = p[1] + p[2] + p[3]
	
def p_expressao(p):
	'''
	expressao : var ATTRIBUTION expressao
			| simples_expressao
	'''
	if len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1]
  
def p_var(p):
	'''
	var : ID
	    | ID BRACKETS expressao BRACKETS
	'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[1] + p[2] + p[3] + p[4]
  
def p_simples_expressao(p):
	'''
	simples_expressao : soma_expressao relacional soma_expressao 
				   | soma_expressao
	'''
	if len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1]
  
def p_relacional(p):
	'''
	relacional : RELOP
	'''
	p[0] = p[1][0]
			
def p_soma_expressao(p):
	'''
	soma_expressao : soma_expressao soma termo
				| termo
	'''
	if len(p) == 3:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1]
  
def p_ariop(p):
	'''
	ariop : ARIOP
	'''
	p[0] = p[1]
 
def p_soma(p):
	'''
	soma : ariop
	'''
	p[0] = p[1]
 
def p_termo(p):
	'''
	termo : termo mult fator
		 | fator
	'''
	if len(p) == 3:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1]
  
def p_mult(p):
	'''
	mult : ariop
	'''
	p[0] = p[1]
 
def p_fator(p):
	'''
	fator : PARENTHESES expressao PARENTHESES
		 | var
		 | ativacao
		 | NUM
	'''
	if len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1]
     
def p_ativacao(p):
	'''
	ativacao : ID PARENTHESES args PARENTHESES
	'''
	p[0] = p[1] + p[2] + p[3] + p[4]
 
def p_args(p):
	'''
	args : arg_lista 
		| vazio
	'''
	p[0] = p[1]
 
def p_arg_lista(p):
	'''
	arg_lista : arg_lista COMMA expressao
			| expressao
	'''
	if len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1]
  
def p_vazio(p):
	'''
	vazio :
	'''
	pass

def p_error(p):
	if p:
		print("Erro sintático na linha %d" % p.lineno)
	else:
		print("Erro sintático na linha %d" % lexer.lineno)


"""
def p_id(p):
	'''
	id : ID
	'''
"""
# O TRECHO ABAIXO ESTÁ NA DOCUMENTAÇÃO DO PLY
# ESTAMOS USANDO APENAS PARA TESTES

# Error rule for syntax errors
# def p_error(p):
# 	print("Syntax error in input!")

# Build the parser
programa = open('gcd.c-', 'r').read()
lexer = regex.lexer
lexer.input(programa)
tokens = regex.tokens

parser = yacc.yacc(debug=True)

try:
	teste = parser.parse(programa, lexer=lexer,debug=True)
	print(teste)
except EOFError:
	print("EOF")
	pass

# while True:
# 	try:
# 		s = input('calc > ')
# 	except EOFError:
# 		break
# 	if not s: continue
# 	result = parser.parse(s)
# 	print(result)

# warnings.warn("Warning...........Message")
