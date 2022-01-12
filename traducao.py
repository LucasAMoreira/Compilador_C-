# =======================================================
#
# Este módulo é responsavel por percorrer a AST e
# traduzir seus nós para uma linguagem intermediária.
#
# =======================================================

global args		# Lista de variáveis de uma função
global var		# Lista de variáveis de uma função
global sp			# Valor do registrador $sp
global argumentos	# Lista de argumentos recebidos por uma função
global comando		# Armazenamos registradores e comando do código MIPS
global aux		# Armazenamos registradores e comando do código MIPS
global iterador	# Usado para ser incrementado e auxiliar
global aux_iter

# Inicialização das variáveis globais
args = []
var = []
sp = 0
argumentos = []
comando = []
aux = []
iterador = 0
aux_iter = 0

# Percorre AST
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
				t_encerra()
				restaura_sp()
			t_return(root)
			#t_encerra(root)
			aux.clear()
			comando.clear()

		elif(root.data == 'fun-declaração'):
			t_function(root)
			comando.clear()

		elif(root.data == 'expressao'):
			comando.clear()
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


# Recebe nó iteracao_decl e gera código MIPS. Também
# invoca t_expr_while para tratar a expressão do laço
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
	pass

# EM DESENVOLVIMENTO
# Recebe nó com valor 'expressao'
# prenche variável global 'comando'
# retorna variável comando
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
		comando.clear()
		t_expr(child)

	if('fim' not in comando and len(comando)==2):
		comando.append('$s1')
		comando.append('fim')

	return comando

# Recebe qualquer nó e gera código 'jr $ra'
def t_return(root):
	res = []
	res.insert(0,'jr')
	res.insert(1,'$ra')
	gera_codigo(res)

# Restaura registrador $sp
def restaura_sp():
	res = []
	res.insert(0,'addi')
	res.insert(1,'$sp')
	res.insert(2,'$sp')
	res.insert(3,str(-1*sp))
	gera_codigo(res)

# Restaura registradores dos argumentos ($aX e $ra)
def t_encerra():
	i=-1*(sp+4)
	j = 0
	register = '$ra'
	while i >= 0:
		res=[]
		res.insert(0,'lw')
		res.append(register)
		res.append(str(i)+'($sp)')
		gera_codigo(res)
		register = '$a'+ str(j)
		i-=4
		j+=1


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
		comando.clear()
		t_expr(root)
	elif(root.data in args):
		index = args.index(root.data)
		aux.insert(0,'move')
		aux.insert(1,'$v0')
		aux.insert(2,'$a'+str(index))
		gera_codigo(aux)
		aux.clear()
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





# EM DESENVOLVIMENTO Gera código em linguagem intermediária
def t_expr(root):

	global i

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

	# Adiciona 'add', 'sub', 'mul' ou 'div' em comando
	if root.data == 'soma_expressao' and root.children[0].data == 'soma_expressao':
		get_operation(root)
		'''
		print(args)
		if(root.data in args):
			print('ROOT')
			indice = args.index(root.data)
			comando.append('$t')
			comando.append('$a'+str(indice))
			gera_codigo(comando)
		'''
	#elif root.data in ['+','-','*','/']:
	#	t_expressao(root)

	#Percorre a árvore
	for child in  (root.children):
		t_expr(child)


	if('else' not in comando and len(comando)==3):
		comando.append('else')

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
	if root.data == 'soma_expressao':
		root.data = 'VISITADO'
	i=0
	res = None
	for child in reversed(root.children):
		for grandchild in (child.children):
			#print(comando)
			percorre(grandchild)
			if len(comando) <= 4:
				comando.insert(1,'$t'+str(i))
			if len(comando) > 4:
				comando.pop(2)

			if len(comando)>=4:
				gera_codigo(comando)
				res = comando[1] # Último registrador
				#print(res)
				comando.clear()
				comando.append(res)
				i+=1

'''
IDEIA
	global temp
	temp = []
	percorre(root,i) # Nova assinatura
	temp.append('$t'+str(i))


'''

def percorre(root):
	if root.data == '+':
		comando.clear()
		comando.insert(0,'add')
		root.data = 'VISITADO'
	elif root.data == '-':
		#comando.clear()
		comando.insert(0,'sub')
		root.data = 'VISITADO'
		#gera_codigo(comando)
	elif root.data == '*':
		#comando.clear()
		comando.insert(0,'mul')
		root.data = 'VISITADO'
		#gera_codigo(comando)
	elif root.data == '/':
		#comando.clear()
		comando.insert(0,'div')
		root.data = 'VISITADO'
		#gera_codigo(comando)
	elif root.data in args:
		indice = args.index(root.data)
		comando.append('$a'+str(indice))
	for child in root.children:
		percorre(child)
