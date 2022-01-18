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
global reg_var
global a
global ops

ops = []

# Inicialização das variáveis globais
args = []
var = []
sp = 0
argumentos = []
comando = []
aux = []
iterador = 0
aux_iter = 0
reg_var = []

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

# Gera código para expressão declaração
# Ex: x = 10; => li $s0, 10
def t_expr_decl(root):

	if root.data == 'expressão-decl':
		root.data = 'VISITADO'

	if root.data.isnumeric():
		if 'add' in comando:
			comando.remove('add')
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
		reg_var.append('$s'+str(index)) # Lista de variáveis

	for child in root.children:
		t_expr_decl(child)
	return comando

# Recebe retorno_decl e gera código 'move $v0, $aX	'
def t_retorno_decl(root):
	res = []
	retorno = False

	if(root.data== 'expressao'):
		comando.clear()
		t_expr(root)
	if root.data == 'ativacao':
		t_ativacao(root)
	elif(root.data in args):
		index = args.index(root.data)
		aux.insert(0,'move')
		aux.insert(1,'$v0')
		aux.insert(2,'$a'+str(index))
		gera_codigo(aux)
		aux.clear()
		return aux

	for child in root.children:
		t_retorno_decl(child)

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
			#print('ARGS: '+str(argumentos))
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
	pass


# EM DESENVOLVIMENTO Gera código em linguagem intermediária
def t_expr(root):

	# Marca nós visitados para eles não serem visitados novamente por t_traduz
	if root.data == 'expressao':
		root.data = 'VISITADO'

	# Adiciona comando de acordo com expressão
	if root.data == 'EQ':
		comando.insert(0,'bne')
	elif(root.data == 'NE'):
		comando.insert(0,'beq')
	elif root.data == '0':
		comando.append('$zero')
	elif root.data in ['>','<','>=','<=']:
		comando.clear()
		comando.insert(0,'slt')
	elif(root.data in args):
		indice = args.index(root.data)
		comando.append('$a'+str(indice))

	# Adiciona 'add', 'sub', 'mul' ou 'div' em comando
	if root.data == 'soma_expressao' and root.children[0].data == 'soma_expressao':
		global reg
		reg=get_operation(root)

	#Percorre a árvore
	for child in  (root.children):
		t_expr(child)

	if('else' not in comando and len(comando)==3):
		comando.append('else')

	return comando

# Gera código com comando 'move', preenchendo os registradores $aX
# Recebe um nó (root), uma lista com o comando (move) e a iteração atual (i)
def aux_ativacao(root,move,i):
	if root.data in args:
		move.append('$a'+str(args.index(root.data)))
		if len(move) == 3:
			gera_codigo(move)
		root.data ='VISITADO'

	if root.data in var:
		move.append('$s'+str(var.index(root.data)))
		if len(move) == 3:
			gera_codigo(move)
			move.clear()
			move.append('move')
			move.append('$a'+str(i+1))
		root.data ='VISITADO'

	for child in root.children:
		aux_ativacao(child,move,i)

	pass

# Gera código MIPS para invocação de funções
def t_ativacao(root):
	# Preenche args com os argumentos da função. EX: args = ['u','v']
	get_args(root)

	if root.data=='ativacao':
		# Preenche argumentos da função
		i = 0
		for arg in args:
			move = []
			move.append('move')
			move.append('$a'+str(i))
			local = aux_ativacao(root,move,i)

			global reg
			if reg and len(move)==2:
				move.append(reg)
				gera_codigo(move)
				reg = None
			i += 1 # Agora deve inserir em list de acordo com a situação
	# Invoca função
	res = []
	if root.data=='ativacao':
		res.insert(0,'jal')
		root.data='VISITADO'
	for child in root.children:
		t_ativacao(child)

	if res:
		res.insert(1,root.children[0].data)
	gera_codigo(res)

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

	if i-1 >= 0:
		return '$t'+str(i-1)


def percorre(root):
	if root.data == '+':
		comando.insert(0,'add')
		root.data = 'VISITADO'
	elif root.data == '-':
		comando.insert(0,'sub')
		root.data = 'VISITADO'
	elif root.data == '*':
		comando.insert(0,'mul')
		root.data = 'VISITADO'
	elif root.data == '/':
		comando.insert(0,'div')
		root.data = 'VISITADO'
	elif root.data in args:
		indice = args.index(root.data)
		comando.append('$a'+str(indice))
	for child in root.children:
		percorre(child)


# Recebe como argumento lista 'codigo'
# Escreve código MIPS no arquivo 'codigo.asm'
def gera_codigo(codigo):
	fim = " "
	arquivo = open("codigo.asm","a")

	k = 0
	# Percorre lista codigo
	if codigo and '$' not in codigo[0]:
		while k < len(codigo):
			# Adiciona vírgula se não é o primeiro nem o último elemento
			if k>0 and k< len(codigo)-1:
				fim=", "
			#print(codigo[k], end=fim)
			cod = str(codigo[k])+fim
			arquivo.write(cod)
			fim =" "
			k+=1
		if codigo != []:
			#print()
			arquivo.write("\n")
		arquivo.close()
