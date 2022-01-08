# ======================================================= 
#
# Este módulo é responsavel por percorrer a AST e 
# traduzir seus nós para uma linguagem intermediária.
#
# =======================================================

global args
global var
global sp
global argumentos
global flag # Uso geral
flag = False

args = []
var = []
argumentos = []
sp=0

global comando
comando = []

global aux
aux = []

# Percorre AST
# Caso o nó seja 'soma_expressao' invoca o método t_tranlate
def t_traduz(root):
	if root:
		if(root.data == 'ativacao'):
			t_ativacao(root)
			
		elif(root.data == 'expressão-decl'):			
			t_expr_decl(root)			
			if  len(comando)>1 and len(comando)<=4:
				if comando[0].find('$') == -1:
					gera_codigo(comando)
			comando.clear()
			
		elif(root.data == 'iteracao_decl'):
			t_iteracao_decl(root)
			if len(comando)>1 and len(comando)<=4:
				gera_codigo(comando)
			comando.clear()
			
		elif(root.data == 'retorno_decl'):			
			t_retorno_decl(root)
			if len(comando)>1 and len(comando)<=4:
				gera_codigo(comando)
				comando.clear()
			
			if sp!=0:
				restaura_sp()
			t_return(root)
			#t_encerra(root)
			aux.clear()
			comando.clear()
			
		elif(root.data == 'fun-declaração'):
			t_function(root)
			comando.clear()
			
		elif(root.data == 'expressao'):				
			t_expr(root)
			if len(comando)>1 and len(comando)<=4:
				gera_codigo(comando)
			comando.clear()
			
		elif(root.data == 'local-declarações'):
			get_vars(root)
			
			
		elif(root.data == 'else'):
			gera_codigo(['else:'])

		elif(root.data == 'params'):
			t_params(root)
			get_params(root)
			comando.clear()
		#elif(root.data == 'args'):
		#	argumentos.clear()
		#	get_args(root)
		#	print(argumentos)
		#	t_args(root)
			
		for child in root.children:
			t_traduz(child)			
	return root

def t_iteracao_decl(root):
	if(root.data == 'while'):
		gera_codigo(['while:'])
	if(root.data == 'expressao'):
		t_expr_while(root)
		if len(comando)>1 and len(comando)<4:
				gera_codigo(comando)
				comando.clear()
	for child in root.children:
		t_iteracao_decl(child)

def get_args(root):	
	for child in root.children:
		if child.children == [] and child.data != ',':
			argumentos.append(child.data)
									
	for child in root.children:
		args = get_args(child)

def t_args(root):
	if(root.data in args):
		print('Tô aqui')
	for child in root.children:
		t_args(child)


def var_count(root):	
	n_var = 0
	if root.data=='var-declaração':
		return 1
		
	for child in root.children:
		n_var += var_count(child)	
	return n_var

def get_vars(root):	
	if root.data=='var-declaração':
		for child in root.children:
			if child.children == [] and child.data != ';':
				var.append(child.data)
									
	for child in root.children:
		get_vars(child)


def t_expr_decl(root):
	
	if root.data == 'expressão-decl':
		root.data = 'VISITADO'
	
	if root.data.isnumeric():
		comando.insert(0,'li')
		comando.append(root.data)
			
	elif root.data == '+':
		comando.insert(0,'add')		
	elif root.data == '-':
		comando.insert(0,'sub')		
	elif root.data == '*':
		comando.insert(0,'mul')
	elif root.data == '/':
		comando.insert(0,'div')
	

		
	if root.data in var:
		index = var.index(root.data)
		comando.append('$s'+str(index))
				
	for child in root.children:
		t_expr_decl(child)
	return comando

	

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
	
	#if root.data == 'expressao':
	#	print('EXPR')
	#	aux=t_expr(root)
	
	'''
	if(root.children == [] and root.data != 'return'):
		# Se retorna um dos argumentos recebidos
		if(root.data in args):
			index = args.index(root.data)
			aux.insert(0,'move')
			aux.insert(1,'$v0')
			aux.insert(2,'$a'+str(index))
			return aux
	'''
	if(root.data== 'expressao'):
		t_expr(root)
	elif(root.data in args):
		index = args.index(root.data)
		aux.insert(0,'move')
		aux.insert(1,'$v0')
		aux.insert(2,'$a'+str(index))
		return aux
	'''
	if(root.data == 'expressao'):
		retorno = True
	'''
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
		
	#gera_codigo(res)
	return aux	
	
		
	
	

	
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


# Gera código MIPS para os parâmetros
def t_encerra(root):
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
			res.insert(0,'lw')
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
			
	elif root.data == '+':
		comando.clear()
		comando.insert(0,'add')		
	elif root.data == '-':
		comando.clear()
		comando.insert(0,'sub')	
	elif root.data == '*':
		comando.clear()
		comando.insert(0,'mul')
	elif root.data == '/':
		comando.clear()
		comando.insert(0,'div')
		
	elif root.data in ['>','<','>=','<=']:	
		comando.clear()
		comando.insert(0,'slt')
	#elif root.data in ['+','-','*','/']:		
	#	t_expressao(root)
		
	#Percorre a árvore 
	for child in  (root.children):				
		t_expr(child)
		
	
	if('else' not in comando and len(comando)==3):
		comando.append('else')	
	
	return comando	

# EM DESENVOLVIMENTO Gera código em linguagem intermediária			
def t_expr_while(root):
	# Marca nós visitados para eles não serem visitados novamente por t_traduz
	if root.data == 'expressao':
		root.data = 'VISITADO'
	
	if root.data == 'EQ':
		comando.insert(0,'bne')	
	elif(root.data == 'NE'):	
		comando.insert(0,'beq')
	elif root.data == '0':
		comando.append('$zero')
	elif root.data in ['>','<','>=','<=']:	
		comando.clear()
		comando.insert(0,'slt')

	#Percorre a árvore 
	for child in  (root.children):				
		t_expr(child)		
	
	if('fim' not in comando and len(comando)==2):
		comando.append('$s1')
		comando.append('fim')	
	
	return comando	
	

		
def t_expressao(root):
	# Marca nós visitados para eles não serem visitados novamente por t_traduz
	if root.data == 'expressao':
		root.data = 'VISITADO'
		
	if root.data == '+':
		comando.insert(0,'add')
		gera_codigo(comando)		
	elif root.data == '-':
		comando.clear()
		comando.insert(0,'sub')
		gera_codigo(comando)	
	elif root.data == '*':
		comando.clear()
		comando.insert(0,'mul')
		gera_codigo(comando)
	elif root.data == '/':
		comando.clear()
		comando.insert(0,'div')
		gera_codigo(comando)
	elif root.data == '0':
		comando.append('$zero')
	elif(root.data in args):		
		indice = args.index(root.data)
		comando.append('$a'+str(indice))				

	# Percorre a árvore 
	for child in reversed(root.children):		
		t_expressao(child)
				
	return comando	
		
		
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
	arquivo = open("codigo.asm","a")
	
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
				cod = array[j]+fim
				arquivo.write(cod)
				fim = " "
				j+=1
			codigo.insert(i,array[1])
			codigo.pop(i+1)
			arquivo.write("\n","a")			
			print()	
		i+=1
	
	# Imprime código
	k = 0							
	while k < len(codigo): 
		if k>0 and k< len(codigo)-1:
			fim=", " 
		print(codigo[k], end=fim)
		
		cod = str(codigo[k])+fim
		arquivo.write(cod)
		fim =" "
		k+=1
	if codigo != []:
		print()
		arquivo.write("\n")
	arquivo.close()

def get_operation(root):
	if(root.data in ['+','-','/','*']):
		print('É TRUEEEEEEEE')
		is_arit = True
	elif(root.data in ['EQ','NE']):
		is_arit= False
	for child in root.children:
		is_arit=get_operation(child)
	return is_arit
	
	
