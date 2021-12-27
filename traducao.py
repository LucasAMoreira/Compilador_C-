#
# Este módulo é responsavel por percorrer a AST e 
# traduzir seus nós para uma linguagem intermediária.
#
# =======================================================


def t_traduz(root):
	if root:
		if(root.data == 'expressao'):	
			#op = get_operation(root)
			#if(op):
			#	print(op)
			t_translate(root)
		for child in root.children:
			t_traduz(child)			
	return root

# Retorna OPERAÇÃO (não os números ou ids)
def get_operation(root):

	for child in root.children:
		if(child.data != 'expressao'):			
			if child.data == '=':
				return('LOAD')
			if child.data == '+':
				return('ADD')
			if child.data == '*':
				return('MULT')
			if child.data == '/':
				return('DIV')
			
def t_translate(root):
	if root.data == 'expressao':
		root.data = 'VISITADO'
	res = []
	registrador = None
	registrador2  = None
	for child in root.children:
		if child.data == '=':
			res.insert(0,'LOAD')
			registrador = '$t1'
		elif child.data == '+':
			res.insert(0,'ADD')
			registrador = '$t0'
		elif child.data == '*':
			res.insert(0,'MULT')
		elif child.data == '/':
			res.insert(0,'DIV')				
		elif child.data == 'expressao':
			registrador2 = t_translate(child)
		elif len(root.children) == 1:
			res.append('ADD')
			res.append(child.data)
			res.append('zero')
			registrador = '$t2'
		else:
			if(child.data.isnumeric()):
				res.append(child.data)
	if registrador2 != None:
		res.append(registrador2)
	if registrador != None:
		res.insert(1,registrador)
	
	print(res)			
	return registrador

'''

FUNÇÃO:
	get_operation()
				

'''	
	
	
	
