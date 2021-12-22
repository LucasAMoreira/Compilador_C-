import ply.yacc as yacc
import ply.lex as lex
import regex


precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    )

def p_programa(p):
	'programa : declaracao_lista'
	p[0] = ('programa',p[1])

def p_declaracao_lista(p):
	'''
	declaracao_lista : declaracao_lista declaracao
				| declaracao
	'''
	if len(p) == 3:
		p[0] = p[1] + p[2]
		p[0] = ('declaração-lista',p[1],p[2])
	else:
		p[0] = p[1]
		p[0] = ('declaração-lista',p[1])
 
def p_declaracao(p):
	'''
	declaracao : var_declaracao
			| fun_declaracao
	'''
	p[0] = p[1]
	p[0] = ('declaração',p[1])
 
def p_var_declaracao(p):
	'''
	var_declaracao : tipo_especificador ID SEMICOLON	
				| tipo_especificador ID OBT NUM CBT SEMICOLON
	'''
	if len(p) == 4:
		p[0] = ('var-declaração',p[1],p[2],p[3])
	else:
		p[0] = ('var-declaração',p[1],p[2],p[3])
  
def p_tipo_especificador(p):
	'''
	tipo_especificador : INT
				    | VOID
	'''
	p[0] = ('tipo-especificador',p[1])
  
def p_fun_declaracao(p):
	'''
	fun_declaracao : tipo_especificador ID OP params CP composto_decl
	'''
	p[0] = ('fun-declaração', p[1], p[2], p[3], p[4], p[5], p[6])
 
def p_params(p):
	'''
	params : param_lista
		  | VOID
	'''
	p[0] = ('params',p[1])

def p_param_lista(p):
	'''
	param_lista : param_lista COMMA param
			  | param
	'''	
	if len(p) == 4:
		p[0] = ('param-lista', p[1], p[2], p[3])
	else:
		p[0] = ('param-lista', p[1])
 
def p_param(p):
	'''
	param : tipo_especificador ID 
		 | tipo_especificador ID OBT CBT
	'''
	if len(p) == 3:
		p[0] = ('param', p[1], p[2])
	else:
		p[0] = ('param', p[1], p[2], p[3], p[4])
  
def p_composto_decl(p):
	'''
	composto_decl : OBR local_declaracoes statement_lista CBR
	'''
	p[0] = ('composto-decl', p[1], p[2], p[3], p[4])
	
	
def p_local_declaracoes(p):
	'''
	local_declaracoes : local_declaracoes var_declaracao
				   | vazio
	'''
	if len(p) == 3 and p[1] and p[2]:
		p[0] = p[1] + p[2]
		p[0] = ('local-declarações', p[1], p[2])
	else:
		p[0] = p[1]
		p[0] = ('local-declarações', p[1])
  
def p_statement_lista(p):
	'''
	statement_lista : statement_lista statement
				 | vazio
	'''
	if len(p) == 3:
		p[0] = ('statement-lista', p[1], p[2])
	else:
		p[0] = p[1]
		p[0] = ('statement-lista', p[1])
  
def p_statement(p):
	'''
	statement : expressao_decl
			| composto_decl 
			| selecao_decl 
			| iteracao_decl 
			| retorno_decl
	'''
	p[0] = ('statement', p[1])
 
def p_expressao_decl(p):
	'''
	expressao_decl : expressao SEMICOLON
				| SEMICOLON
	'''
	if len(p) == 3:
		p[0] = ('expressão-decl',p[1], p[2])
	else:
		p[0] = ('expressão-decl',p[1])
  
def p_selecao_decl(p):
	'''
	selecao_decl : IF OP expressao CP statement
			   | IF OP expressao CP statement ELSE statement
	'''
	if len(p) == 6:
		p[0] = ('seleção-decl',p[1], p[2], p[3], p[4], p[5])
	else:
		p[0] = ('seleção-decl',p[1], p[2], p[3], p[4], p[5], p[6], p[7])

def p_iteracao_decl(p):
	'''
	iteracao_decl : WHILE OP expressao CP statement
	'''
	x = ('iteracao_decl',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
 
def p_retorno_decl(p):
	'''
	retorno_decl : RETURN SEMICOLON
			   | RETURN expressao SEMICOLON
	'''
	x = ('retorno_decl',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
	
def p_expressao(p):
	'''
	expressao : var ATTRIBUTION expressao
			| simples_expressao
	'''
	x = ('expressao',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
  
def p_var(p):
	'''
	var : ID
	    | ID OBT expressao CBT
	'''
	x = ('var',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
  
def p_simples_expressao(p):
	'''
	simples_expressao : soma_expressao relacional soma_expressao 
				   | soma_expressao
	'''
	x = ('simples_expressao',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
  
def p_relacional(p):
	'''
	relacional : RELOP
	'''
	p[0] = ('relacional', p[1])
			
def p_soma_expressao(p):
	'''
	soma_expressao : soma_expressao soma termo
				| termo
	'''
	x = ('soma_expressao',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
  
 
def p_soma(p):
	'''
	soma : PLUS
		| MINUS
	'''
	p[0] = ('soma',p[1])
 
def p_termo(p):
	'''
	termo : termo mult fator
		 | fator
	'''
	x = ('termo',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
  
def p_mult(p):
	'''
	mult : TIMES
		| DIVIDE
	'''
	p[0] = ('mult', p[1])
 
# MODIFICADO 
def p_fator(p):
	'''
	fator : OP expressao CP
		 | var
		 | ativacao
		 | NUM
		 | soma NUM
	'''
	x = ('fator',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
     
def p_ativacao(p):
	'''
	ativacao : ID OP args CP
		   
	'''
	x = ('ativacao',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
 
def p_args(p):
	'''
	args : arg_lista 
		| vazio
	'''
	p[0] = ('args', p[1])
 
def p_arg_lista(p):
	'''
	arg_lista : arg_lista COMMA expressao
			| expressao
	'''
	x = ("arg_lista",)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x

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

tokens = regex.tokens
parser = yacc.yacc(debug=True)

