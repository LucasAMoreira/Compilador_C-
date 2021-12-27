import Quad
from traducao import *
from astree import *
from simple import *
	
	
# ================================================ 	

	

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
		l=[]
		i=0
		while i<len(c):
			if(c[i]!=';'):
				r.append(c[i])
			else:
				l.append(r)
				r=[]
			i+=1
		resposta.append(l)
					
	return resposta

def ordena(lista):
	resposta=[]
	# Para cada lista de listas
	for c in lista:
		r=[]
		l=[]	
		i=len(c)-1
		while i>=0:
			r.append(c[i])
			i-=1
		l.append(r)
		resposta.append(l)
			
	return resposta	

def padding(lista):
	resposta=[]
	for d in lista:
		l=[]
		for c in d:
			r=c
			i=0
			while len(r)<4:
				r.insert(1,'$')
			l.append(r)
		resposta.append(l)
	return resposta

'''
def simplifica(lista):
	resposta=[]
	for d in lista:
		for c in d:
			for b in c:
				resposta.append(b)
	return resposta
'''
def conta(lista):
	resposta=0
	for c in lista:
		i=0
		while i<len(c):
			if(c[i]=='LOAD'):
				resposta +=1;
				break
			if(c[i]=='$'):
				resposta +=1	
			i+=1		
	return resposta

def addTemp(lista):

	resposta =[]
	t=conta(lista)
	temp = []
	i=0
	while i<t:
		temp.append('$t'+str(i))
		temp.append('$t'+str(i))
		i+=1
	j=0
	for c in lista:
		r=c
		i=0
		while i<len(c):
			if(c[i]=='LOAD'):
				r[i+1]=temp[j]				
				break
			if(c[i]=='$'):
				r[i]=temp[j]
			i+=1		
			j+=1
		resposta.append(r)
	return resposta

def geraCod(lista):
	for d in lista:
		if '$' in d:
			d.remove('$')
		d = " ".join(d)
		print(d, end=";\n")


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
		



		
		
		
		
		
	
