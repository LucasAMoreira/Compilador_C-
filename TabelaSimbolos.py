class Elemento:

	def __init__(self,lexeme,nome,atributo):
		self.lexeme=lexeme
		self.nome=nome
		self.atributo=atributo

class TabelaSimbolos:
	tabela = []
	
	def adiciona(self,lexeme, nome, atributo):
		novo = Elemento(lexeme,nome,atributo)
		self.tabela.append(novo)
	
	def imprime(self):
		for elemento in self.tabela:
			print(elemento.lexeme,elemento.nome,elemento.atributo)
