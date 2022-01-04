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
		if(root.data == 'return'):
			t_return(root)
		elif(root.data == 'expressao'):	
			t_translate(root)
		elif(root.data == 'fun-declaração'):
			t_function(root)
		elif(root.data == 'seleção-decl'):
			t_if(root)
		
		for child in root.children:
			t_traduz(child)			
	return root

# Recebe nó com 'return' e gera código 'jr $ra'
def t_return(root):
	res = []
	res.insert(0,'jr')
	res.insert(1,'$ra')
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
	
def t_function(root):
	# Marca nós visitados para eles não serem visitados novamente por t_traduz
	if root.data == 'soma_expressao':
		root.data = 'VISITADO'
	
	# Armazenamos em res o comando em linguagem intermediária
	res = []
	registrador = None
	registrador2  = None
	
	i=1;# adicionado 27/12
	
	if(root.data == 'fun-declaração'):
		for child in root.children:
			if child.children == [] and child.data != '(' and child.data != ')':
				res.insert(0,"\n"+child.data+":")
		
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
		

	
	
	
