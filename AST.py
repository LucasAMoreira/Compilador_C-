import Quad

def retornaTriplas(tupla):
	x=''
	for t in tupla:
		if(type(t)==str):
			if(t=='='):
				x+='LOAD'
		if(type(t)==tuple):
			retornaTriplas(t);

# Recebe uma arvore e altera suas operações
# Ex: '+' -> 'ADD'
def substitute(ast):
	if(ast):
		if(ast.data == '+'):
			ast.data='ADD'
		if(ast.data == '='):
			ast.data='LOAD'
		for children in ast.children:
			substitute(children)
	return ast
		
# Retorna lista de declarações
def retornaOp(ast):
	declaracoes = ''
	if(ast.data=='expressão-decl'):
		expr = retornaExpr(ast);
		return expr
	for children in ast.children:
		expr=retornaOp(children)
		if(expr != ''):
			declaracoes += expr + ' '
	return declaracoes
	
	
def retornaExpr(expr):
	res=''
	if(expr.children==[]):		
		return expr.data
	for children in expr.children:
		expr = retornaExpr(children)
		if(expr!=''):
			res+=' '+expr
	return res


def retornaSep(comandos):
	comandos=comandos.split(';');
	resposta=[]
	for c in comandos:		
		c=c.split(' ')
		r=[]
		i=0
		while i<len(c):
			if(c[i]!=''):
				r.append(c[i])
			i+=1
		resposta.append(r)
	return resposta


def inverte(comandos):
	resposta=[]
	for c in comandos:
		r=[]
		i=0
		t=len(c)-1
		while i<t:			
			r.append(c[i+1])
			r.append(c[i])
			i+=2
			if(i>=t):
				r.append(c[len(c)-1])
		resposta.append(r)
	return resposta

def divide(lista):
	resposta=[]
	for c in lista:
		r=[]
		i=0
		while i<len(c)-1:
			r.append(c[i])				
			if(c[i+1]=='ADD' or c[i+1]=='LOAD' ):
				r.append(';')
			i+=1
			if(i==len(c)-1):
				r.append(c[i])
				r.append(';')
		resposta.append(r)
	return resposta

def separa(lista):
	resposta=[]
	for c in lista:
		r=[]
		i=0
		while i<len(c):
			if(c[i]!=';'):
				r.append(c[i])
				print(c[i])
			else:
				r=[]
			resposta.append(r)
			i+=1
	return resposta

def padding(lista):
	resposta=[]
	for c in lista:
		r=c
		i=0
		while len(r)<4:
			r.insert(1,'$')
		resposta.append(r)
	return resposta

def criaQuad(lista):
	res=[]
	arg1=[]
	arg2=[]
	op=[]
	
	quad = Quad(op.arg1,arg2,result)
	
	
	res = []
	for l in lista:
		i=2
		while(i<len(l)):
			t='$T'
			l.insert(i,t)
			i+=2
		res.append(l)
	return res
		



		
		
		
		
		
	
