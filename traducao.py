# ======================================================= 
#
# Este módulo é responsavel por percorrer a AST e 
# traduzir seus nós para uma linguagem intermediária.
#
# =======================================================


# Percorre AST
# Caso o nó seja 'soma_expressao' invoca o método t_tranlate
def t_traduz(root):
	if root:
		if(root.data == 'ativacao'):
			t_ativacao(root)
		elif(root.data == 'return'):
			t_return(root)
		elif(root.data == 'fun-declaração'):
			t_function(root)
		elif(root.data == 'expressao'):	
			t_expressao(root)
		elif(root.data == 'seleção-decl'):
			t_if(root)
		elif(root.data == 'params'):
			t_params(root)

		for child in root.children:
			t_traduz(child)			
	return root

# Recebe nó com 'return' e gera código 'jr $ra'
def t_return(root):
	res = []
	res.insert(0,'jr')
	res.insert(1,'$ra')
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
	if params > 0:
		sp = (params*-4)-4
		res.insert(0,'addi')
		res.append('$sp')
		res.append('$sp')
		res.append(sp)
		gera_codigo(res)
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




# Gera código MIPS de IF
def t_if(root):
	# Marca nós visitados para eles não serem visitados novamente por t_traduz
	if root.data == 'expressao':
		root.data = 'VISITADO'
	
	tem_else = True
	
	res = []
	
	# Percorre árvore e armazena em res o código intermediário
	if(root.data == 'simples-decl'):
		for child in root.children:
			if child.data == 'else':
				tem_else = True
			else:
				tem_else = False
			
	if tem_else:
		for child in root.children:	
			if child.data == 'EQ':
				res.insert(0,'bne')	
			elif child.children != []:
				t_if(child)
	
	gera_codigo(res)	

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

# Gera código em linguagem intermediária			
def t_translate(root):
	# Marca nós visitados para eles não serem visitados novamente por t_traduz
	if root.data == 'expressao':
		root.data = 'VISITADO'
	
	# Armazenamos em res o comando em linguagem intermediária
	res = []
	registrador = None
	registrador2  = None
	
	i=1;# adicionado 27/12
	
	
	# Percorre árvore e armazena em res o código intermediário
	for child in root.children:
		if child.data == '=':
			res.insert(0,'ld')
			registrador = '$t0'
		elif child.data == '+':
			res.insert(0,'add')
			registrador = '$t0'
		elif child.data == '*':
			res.insert(0,'mul')
		elif child.data == '/':
			res.insert(0,'div')
		elif child.data =='while':
			res.insert(0,'while:')	
		elif child.data == 'return':
			res.insert(0, 'jr $ra')			
		elif child.data == 'expressao':
			registrador2 = t_translate(child)
		elif len(root.children) == 1:
			res.append('li')
			res.append('$t'+str(i))
			res.append(child.data)
		elif child.data.isnumeric():
			res.append(['li', '$t'+str(i),child.data])
			i+=1# adicionado 27/12
			#res.append(child.data)
			#registrador = '$t'+str(i)
			
		
	if registrador2 != None:
		res.append(registrador2)
	if registrador != None:
		res.insert(1,registrador)
	
	gera_codigo(res)	
	#print(res)		
	return registrador
	


	

	
		

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
		

	
	
	
