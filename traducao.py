# ======================================================= 
#
# Este módulo é responsavel por percorrer a AST e 
# traduzir seus nós para uma linguagem intermediária.
#
# =======================================================

global args
global sp
args = []
sp=0

global comando
comando = []

# Percorre AST
# Caso o nó seja 'soma_expressao' invoca o método t_tranlate
def t_traduz(root):
	if root:
		if(root.data == 'ativacao'):
			t_ativacao(root)
		elif(root.data == 'retorno_decl'):
			t_retorno_decl(root)
		elif(root.data == 'fun-declaração'):
			t_function(root)
		elif(root.data == 'expressao'):	
			t_expr(root)
		elif(root.data == 'seleção-decl'):
			t_if(root)
		elif(root.data == 'params'):
			t_params(root)
			get_params(root)

		for child in root.children:
			t_traduz(child)			
	return root

# Recebe qualquer nó e gera código 'jr $ra'
def t_return(root):
	res = []			
	res.insert(0,'jr')
	res.insert(1,'$ra')		
	gera_codigo(res)
	
def restaura_sp():
	res = []
	res.insert(0,'addi')
	res.insert(1,'$sp')
	res.insert(2,'$sp')
	res.insert(3,str(-1*sp))
	gera_codigo(res)
	
# Recebe retorno_decl e gera código 'move $v0, $aX	'
def t_retorno_decl(root):
	res = []	
	retorno = False
	
	if(root.children == [] and root.data != 'return'):
		# Se retorna um dos argumentos recebidos
		if(root.data in args):
			index = args.index(root.data)
			res.insert(0,'move')
			res.insert(1,'$v0')
			res.insert(2,'$a'+str(index))
	if(root.data == 'expressao'):
		retorno = True
	'''
	if(root.data == 'expressao'):
		retorno = True
		for child in root.children:
			
			if(child.data in args):
				index = args.index(child.data)
				res.insert(0,'move')
				res.insert(1,'$v0')
				res.insert(2,'$a'+str(index))
	'''			
	for child in root.children:
		t_retorno_decl(child)
		
	gera_codigo(res)
	
	
	
	if retorno:
		restaura_sp()
		t_return(root)
	
	
# Gera código MIPS para IF
def t_if(root):

	# Resposta
	res = []

	if root.data == 'expressao':
		comando = []
		res=t_expr(root)
	elif(root.data == 'retorno_decl'):
		t_retorno_decl(root)
	elif(root.data == 'else'):
		res.append('else:')
	for child in root.children:	
		t_if(child)
		'''
		if valor:
			if valor == 'bne' or valor == 'beq':
				res.insert(0,t_if(child))
			else:
				res.append(t_if(child))
		'''
		if('else' not in res and len(res)==3):
			res.append('else')	
	if(len(res)>1 and len(res)<5)or 'else:' in res:
		gera_codigo(res)
	
# Recebe um nó 'fun_declaração' e gera rótulo MIPS
# EX: 'funcao()' -> 'funcao:'
def t_function(root):	
	# Armazenamos em res o comando em linguagem intermediária
	res = []
	
	# Percorre os filhos de root
	# Insere 'nome_da_função' + ':' em res
	for child in root.children:
		if child.children == [] and child.data != '(' and child.data != ')':
			res.insert(0,"\n"+child.data+":")
	
	gera_codigo(res)

def get_params(root):
	
	if root.data=='param':
		for child in root.children:
			if child.children == []:
				args.append(child.data)
				
					
	for child in root.children:
		param = get_params(child)
		

# Retorna número de parâmetros de uma função
def params_count(root):	
	params = 0
	if root.data=='param':
		return 1
		
	for child in root.children:
		params += params_count(child)	
	return params

# Gera código MIPS para os parâmetros
def t_params(root):
	params = params_count(root)
	res = []
	# Se é um método void não faz nada
	if params > 0:
		# Salva novo topo da pilha
		global sp
		sp = (params*-4)-4
		res.insert(0,'addi')
		res.append('$sp')
		res.append('$sp')
		res.append(sp)
		gera_codigo(res)
		# Salva registradores na moldura
		i=-1*(sp+4)
		j = 0
		register = '$ra'
		while i>=0:
			res=[]
			res.insert(0,'sw')
			res.append(register)
			res.append(str(i)+'($sp)')
			gera_codigo(res)
			register = '$a'+ str(j)
			i-=4
			j+=1
		

# EM DESENVOLVIMENTO Gera código em linguagem intermediária			
def t_expr(root):
	# Marca nós visitados para eles não serem visitados novamente por t_traduz
	if root.data == 'expressao':
		root.data = 'VISITADO'

	if root.data == 'EQ':
		comando.insert(0,'bne')	
	elif(root.data == 'NE'):
		comando.insert(0,'beq')
	elif root.data == '0':
		comando.append('$zero')
	elif(root.data in args):		
		indice = args.index(root.data)
		comando.append('$a'+str(indice))				

	# Percorre a árvore 
	for child in root.children:		
		t_expr(child)
				
	return comando	
		



		

# EM DESENVOLVIMENTO Gera código em linguagem intermediária			
def t_expressao(root):
	# Marca nós visitados para eles não serem visitados novamente por t_traduz
	if root.data == 'expressao':
		root.data = 'VISITADO'
	
	# Armazenamos em res o comando em linguagem intermediária
	res = []
	registrador = None
	registrador2  = None
	i=0;# adicionado 27/12

	# Percorre árvore e armazena em res o código intermediário
	for child in root.children:	

		if root.data == '/':
			print('DIV')
			res.insert(0,'div')		
		elif root.data.isnumeric():
			res.append(['li', '$s'+str(i),root.data])
			i+=1# adicionado 27/12
			#res.append(child.data)
			#registrador = '$t'+str(i)	
		t_expressao(child)
			
		
	if registrador2 != None:
		res.append(registrador2)
	if registrador != None:
		res.insert(1,registrador)
	
	gera_codigo(res)	
	#print(res)		
	return registrador



# Gera código MIPS para invocação de funções
def t_ativacao(root):
	
	res = []
	if root.data=='ativacao':
		res.insert(0,'jal')
		root.data='VISITADO'
		
	for child in root.children:
		t_ativacao(child)
	if res:
		res.insert(1,root.children[0].data)
	
	gera_codigo(res)


# Recebe como argumento o código intermediário
# Imprime o código como MIPS
def gera_codigo(codigo):

	i=0
	fim = " "
	
	# Percorre código.
	# Caso haja uma lista dentro (EX: 'li'), a imprime primeiro
	while i < len(codigo):
		if type(codigo[i])==list:
			j = 0
			array = codigo[i]
			while j < len(array):
				if j < len(array)-1 and j>0:
					fim = ", "
				print(array[j], end=fim)
				fim = " "
				j+=1
			codigo.insert(i,array[1])
			codigo.pop(i+1)			
			print()	
		i+=1
	
	# Imprime código
	k = 0							
	while k < len(codigo): 
		if k>0 and k< len(codigo)-1:
			fim=", " 
		print(codigo[k], end=fim)
		fim =" "
		k+=1
	if codigo != []:
		print()
		

	
	
	
