#
# Este módulo possui métodos que simplificam uma árvore
#
# ======================================================

from astree import *

# Recebe ast e retorna versão simplificada
def simple_ast(root):
	if root:
		if(root.data == 'soma_expressao'):	
			simple_expressao(root,root)
			del_parents(root)
		for child in root.children:
			simple_ast(child)			
	return root

# Simplifica parte da árvore
def simple_expressao(ast, expr):	
	if expr:
		t = len(expr.children)
		if(expr.children == [] and expr.parent.data != 'soma_expressao'):
			novo = TreeNode(expr.data)
			ast.add_child(novo)
		i=0
		while i < t:
			child = expr.children[i]
			if child.data != 'expressao':
				simple_expressao(ast, child)
			i+=1
	return ast

# Apaga nós com filhos	
def del_parents(ast):
	i = 0
	while i< len(ast.children):
		if(ast.children[i].children != [] and ast.children[i].data != 'expressao'):
			ast.children.pop(i)
		i+=1
	


