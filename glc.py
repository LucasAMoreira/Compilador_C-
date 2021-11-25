import ply.yacc as yacc
import ply.lex as lex
# from regex import tokens
import regex
# from AST import *
import warnings
import sys

AST = AST()

def p_programa(p):
	'programa : declaracao_lista'
	#p[0] = p[1]
	p[0] = ('programa',p[1])
	global raiz
	raiz = p[0]
	
 
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
	x=[]
	i=1
	while(i<len(p)):
		x.append(p[i])
		i=i+1 
	if len(p) == 4:
		p[0] = x #p[1] + p[2] + p[3]
		p[0] = ('var-declaração',p[1],p[2],p[3])
	else:
		p[0] = x #p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
		p[0] = ('var-declaração',p[1],p[2],p[3])
  
def p_tipo_especificador(p):
	'''
	tipo_especificador : INT
				    | VOID
	'''
	p[0] = p[1]
	p[0] = ('tipo-especificador',p[1])
  
def p_fun_declaracao(p):
	'''
	fun_declaracao : tipo_especificador ID OP params CP composto_decl
	'''
	x=[]
	x.append(p[1])
	x.append(p[2])
	x.append(p[3])
	x.append(p[4])
	x.append(p[5])
	x.append(p[6])	
	p[0] = x
	#p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
	p[0] = ('fun-declaração', p[1], p[2], p[3], p[4], p[5], p[6])
 
def p_params(p):
	'''
	params : param_lista
		  | VOID
	'''
	p[0] = p[1]
	p[0] = ('params',p[1])

def p_param_lista(p):
	'''
	param_lista : param_lista COMMA param
			  | param
	'''
	x=[]
	i=1
	while(i<len(p)):
		x.append(p[i])
		i=i+1 
	
	if len(p) == 4:
		p[0] = x #p[1] + p[2] + p[3]
		p[0] = ('param-lista', p[1], p[2], p[3])
	else:
		p[0] = x #p[1]
		p[0] = ('param-lista', p[1])
 
def p_param(p):
	'''
	param : tipo_especificador ID 
		 | tipo_especificador ID OBT CBT
	'''
	x=[]
	i=1
	while(i<len(p)):
		x.append(p[i])
		i=i+1 
		
	if len(p) == 3:
		p[0] = x #p[1] + p[2]
		p[0] = ('param', p[1], p[2])
	else:
		p[0] = x #p[1] + p[2] + p[3] + p[4]
		p[0] = ('param', p[1], p[2], p[3], p[4])
  
def p_composto_decl(p):
	'''
	composto_decl : OBR local_declaracoes statement_lista CBR
	'''
	#	print("########################################################")
	#	print(p[1])
	#	print(p[2])
	#	print(p[3])
	#	print(p[4])
	x=[]
	x.append(p[1])
	x.append(p[2])
	x.append(p[3])
	x.append(p[4])
	p[0] = x
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
		x = []
		x.append(p[1])
		x.append(p[2])
		p[0]=x	
		#p[0] = p[1] + p[2]
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
	p[0] = p[1]
	p[0] = ('statement', p[1])
 
def p_expressao_decl(p):
	'''
	expressao_decl : expressao SEMICOLON
				| SEMICOLON
	'''
	x=[]
	i=1
	while(i<len(p)):
		x.append(p[i])
		i=i+1 

	if len(p) == 3:
		p[0] = x #p[1] + p[2]
		p[0] = ('expressão-decl',p[1], p[2])
	else:
		p[0] = x #p[1]
		p[0] = ('expressão-decl',p[1])
  
def p_selecao_decl(p):
	'''
	selecao_decl : IF OP expressao CP statement
			   | IF OP expressao CP statement ELSE statement
	'''
	x=[]
	i=1
	while(i<len(p)):
		x.append(p[i])
		i=i+1 
	if len(p) == 6:		
		p[0] = x #p[1] + p[2] + p[3] + p[4] + p[5]
		p[0] = ('seleção-decl',p[1], p[2], p[3], p[4], p[5])
	else:
		p[0] = x #p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]
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
  
def p_ariop(p):
	'''
	ariop : ARIOP
	'''
	p[0] = ('ariop', p[1])
 
def p_soma(p):
	'''
	soma : ariop
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
	mult : ariop
	'''
	p[0] = ('mult', p[1])
 
# MODIFICADO 
def p_fator(p):
	'''
	fator : OP expressao CP
		 | var
		 | ativacao
		 | NUM
	'''
	x = ('fator',)
	for i in p[1:]:
		x = x + (i,)
	p[0] = x
     
def p_ativacao(p):
	'''
	ativacao : ID OP args CP
		    | ID OP CP
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
"""

/* COMENTÁRIO */
int vazio(void){
	if (1<2){
		int x;
		x = 0;
	}else{
		return 1;
	}
	int y;
	y = 2/3*4;
	return 0;
}
"""
"""
programa = 
/* Um programa para calcular o mdc
   segundo o algoritmo de Euclides */  
    
   int gcd (int u, int v){
      if (v==0) return u;
      else return gcd(u,v,1);
      /* u-u/v*v == u mod v */
   }
"""

lexer = regex.lexer

# Nome do arquivo de entrada do lexer
parametro = sys.argv[1]

# Abre arquivo e armazena seu conteúdo na variável 'programa'
arq = open(parametro,'r')
programa = arq.read();

lexer.input(programa)
tokens = regex.tokens

parser = yacc.yacc(debug=True)

try:
	teste = parser.parse(programa, lexer=lexer,debug=True)
	print(teste)
	print("######################")
except EOFError:
	print("EOF")
	pass
arq.close();
# while True:
# 	try:
# 		s = input('calc > ')
# 	except EOFError:
# 		break
# 	if not s: continue
# 	result = parser.parse(s)
# 	print(result)

# warnings.warn("Warning...........Message")
