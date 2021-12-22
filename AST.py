'''

class Node:	
	tipo = "" # Terminal ou não terminal
	valor = "NT"
	ID =	-1
	noFilho = -1

	def __init__(self, tipo, valor, ID, noFilho):
		self.tipo = tipo
		self.valor= valor
		self.ID = ID
		self.noFilho = noFilho

class AST:
	raiz = Node("NT","NT",-1,-1);
	
	def add(pai,tipo,valor):
		filho = Node(tipo, valor, pai.ID, -1)
		pai.noFilho = filho
	
	def __init__(self, valor):
		self.raiz= Node("nt",valor, 0,-1)
		
		
	def imprime(self):
		print(self.raiz.valor)
		print(self.raiz.noFilho)

'''


	
'''
def retornaAST(tupla):
	for e in tupla:
		if(type(e)==str):
			print(e)

		if(type(e)==tuple):
			retornaAST(e)	
'''
'''
def retornaAST(tupla, i):

	for e in tupla:		
		if(type(e)==str):
			print(e, end=" ")

		if(type(e)==tuple):
			i=i+1
			print('')
			print('├'+'─'*i, end="")
			retornaAST(e,i)	
'''	
'''
def retornaAST(tupla, i):
	flag=0
	for e in tupla:

		if(e=='soma_expressao'):
			flag=1
		if(flag==1):
			print(e)

		if(type(e)==tuple):
			retornaAST(e,i)
'''			

class No:
	def __init__(self,valor,filhos):
		self.valor=valor
		self.filhos=filhos

def criaAST(tupla):
	if(type(tupla[1])==tuple):
		no = No(tupla[0],criaAST(tupla[1]))
	if(type(tupla[1])==str):
		for t in tupla:
			no = No(t,None)

	return no	
		
	
	#tupla = criaAST(tupla[1])
	#filho = No(tupla,tupla[1])
	return no
	'''
	if(type(t)==str):
		no = No(t,None)
	if(type(t)==tuple):
		filho = No(t,None)
		no.filho=filho
		return criaAST(t)
	return no
	'''	
	'''	
		RAIZ
		|	FILHO
		|	|	NETO1
		|	|	NETO2
		|	|	|	BISNETO1
		|	|	|	BISNETO2
		|	|	NETO3
		
		Se o próximo é tupla, então é filho
		Se é str é irmão
	'''		

			

def printAST(raiz):
	print(raiz.valor)
	if(raiz.filhos != None):
		printAST(raiz.filhos)


# Get operation
#def retornaAST(tupla):
#	no = No(tupla[0],None)
#	for(e)
#	if(len(tupla)==2):
#		no.filho=retornaAST(tupla[1])
#	return no



		
		
def percorre(tupla, op, arg1, arg2):
	for e in tupla:
		if(e=='='):
			op.append(e)
		if(type(e)==tuple):
			if(e[0]=='var'):
				arg1.append(e[1])
			if(e[0]=='fator'):
				arg2.append(e[1])
			if(e[0]=='soma'):
				op.append(e[1])					
			percorre(e,op,arg1,arg2)	

def quadLoad(op,arg1,arg2,result):
	i=0
	while(i<len(op)):
		if(op[i]=='='):
			op[i]='LOAD';
			result.append(arg1[i])
			arg1[i]=arg2[i]
			arg2[i]=None
		i=i+1

def quadPreLoad(op,arg1,arg2,result):
	i=0
	while(i<len(op)):
		if(op[i]=='='):
			op[i]='LOAD';
			if(op[i+1]!='='):
				arg1.insert(i+1,'TEMP')
			result.append(arg1[i])
			arg1[i]=arg2[i]
			arg2[i]=None
		i=i+1
		
def quadInv(op,arg1,arg2,result):
	i=0
	while(i<len(op)):
		if(op[i]=='+' or op[i]=='-'):
			
			op[i]='LOAD';
			result.append(arg1[i])
			arg1[i]=arg2[i]
			arg2[i]=None
		i=i+1
		
def quadSoma(op,arg1,arg2,result):
	i=0
	while(i<len(op)):
		if(op[i]=='+'):
			op[i]='ADD';
			arg2[i]=arg1[i+1]
			arg1.pop(i+1)
		i=i+1
			

#class Quad:
#	op=[]
#	arg1=[]
#	arg2=[]
#	result=[]
#	
#	def __init__(self):
		
	

			
			
		
		
		
		
		
		
		
		
		
		
		
		

