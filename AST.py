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
	if(ast.data == '+'):
		ast.data='ADD'
	if(ast.data == '='):
		ast.data='LOAD'
	for children in ast.children:
		substitute(children)
	return ast
	
# Retorna lista de declarações
def addTemp(ast):
	declaracoes = []
	if(ast.data=='expressão-decl'):
		expr = retornaExpr(ast);
		#declaracoes.append(expr)
		return expr
	for children in ast.children:
		expr=addTemp(children)
		declaracoes.append(expr)
	return declaracoes
	
	
def retornaExpr(expr):
	res=''
	if(expr.children==[]):		
		return expr.data
	for children in expr.children:
		expr = retornaExpr(children)
		res+=' '+expr
	return res








		
		
		
		
		
	
