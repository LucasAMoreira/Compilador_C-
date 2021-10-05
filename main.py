import regex
import ply.lex as lex

lexer = lex.lex(module=regex);

# Test it out
#data =  'var=50; /*\'COMENTÁRIO\' EOF eof */ \nif(var>&5){\n\tvar = var + 1;\n}'

data = """

/*/*
 Um programa para calcular o mdc
   segundo o algoritmo de Euclides.
*/
   
   int gcd (int u, int v){
      if (v==0) return u;
      else return gcd(v,u-u/v*v);
      /* u-u/v*v == u mod v */
   }
   
"""

print(data)
 # Give the lexer some input
lexer.input(data)
 
# Tokenize
i=0
while True:
     tok = lexer.token()
     if not tok: 
         break      # No more input
     print(tok.value, tok.type,tok.lineno)
     i=i+1
     
print(i)



