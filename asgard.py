#!/usr/bin/python
# interpretador lexico 
# Gustavo Ortega 09-10590
# Juliana Leon 08-10608

from ply.lex import TOKEN

import ply.lex as lex
import ply.yacc as yacc
import sys

# lista de tokens reservados
reserved = {
		'using' : 'TkUsing', 'of type' : 'TkOfType', 'integer' : 'TkInteger', 'boolean' : 'TkBoolean', 'canvas' : 'TkCanvas',
		'begin' : 'TkBegin', 'from' : 'TkFrom', 'while' : 'TkWhile', 'to' : 'TkTo', 'repeat' : 'TkRepeat', 'with' : 'TkWith',
		'if' : 'TkIf', 'else' : 'TkElse', 'done' : 'TkDone', 'end' : 'TkEnd', 'then' : 'TkThen', 'read' : 'TkRead',
		'print' : 'TkPrint', 'true' : 'TkTrue', 'false' : 'TkFalse'
		}

# lista de tokens 

tokens = [
		'TkComa','TkPuntoYComa','TkParAbre','TkParCierra','TkLienzo','TkIdent','TkNum','TkSuma','TkResta','TkMult',
		'TkDiv','TkMod','TkConjuncion','TkDisyuncion','TkNegacion','TkMenor','TkMenorIgual','TkMayor','TkMayorIgual',
		'TkIgual','TkDesIgual','TkHorConcat','TkVerConcat','TkRot','TkTras','TkAsignacion',
		] + list(reserved.values())



# defincion para reconocer el token TkOfType
ab1	= r'of([\s\n\t]+ |{-[^\\]*-} )+type'

@TOKEN(ab1)
def t_ID(t):
	t_ID.__doc__ = ab1
	t.type = reserved.get(t.value,'TkOfType')
	for i in range(0,len(t.value)):
		if (t.value[i] == '\n'):
			t.lexer.lineno += 1
	return t

# definicion obtener el numero de lineas leidas
def t_newline(t):
	r'\n'
	t.lexer.lineno += 1


# definicion para ignorar comentarios
def t_COMMENT(t):
	#r'{-[ 0-9a-zA-Z<>/:=\\?\+\*#%()\[\]\t\n,;\.}{!"]*|[ 0-9a-zA-Z<>/:=\\?\+\*#%()\[\]\t\n,;\.}{!"]*-}'
	r'{-[^\\]*-}'	
	for i in range(0,len(t.value)):
		if (t.value[i] == '\n'):
			t.lexer.lineno += 1
	pass	
# definicion de expresiones

def t_TkNum(t):
	r'[0-9]+'
	try:
		t.value = int(t.value)
	except ValueError:
		print 'Error de decimal'
	return t

def t_TkIdent(t):
	r'[a-zA-Z0-9]+'
        t.type = reserved.get(t.value,'TkIdent')
        if (t.type == reserved.get(t.value,'reserved')):
	  return t
	else:
	  return t

def t_TkLienzo(t):
	r'<([/]|[\\]|[\-]|[_]|[ ]|[|]|empty)>' 
	return t

# definicion para saber en que columna se encuentra un caracter
# referencia a  http://mmandrille.googlecode.com/svn-history/r4/compiladores/Version_Final/Pascal_Lex.py, 
# se realizaron los ajustes necesarios a nuestra implementacion
def column(input,token):
    i = token.lexpos
    j = 0
    k = 0  
    while i > 0:
        if input[i] == '\n':
		break
        if input[i] == '\t': 
            	k +=1        #si el caracter es un tab tengo un contador para la cantidad de tabs
        i -=1                #resta la cantidad de caracteres (no se considera tab como 8 caracteres, sino como uno solo) desde la columna 					relativa (la que maneja python) del token hasta el principio de la linea del token
    if (token.lineno == 1):
        k +=0
        j = 0
    else:
        j = 1
    column = ((((token.lexpos - i) + (k*8)) - k) - j) +1     #formula que calcula las columnas
    return column



t_ignore = ' \t'

def t_error(t):
	print ("Error: Caracter inesperado %s en la fila %d columna %s " % (t.value[0],t.lineno,column(archi,t)))
	lexer.skip(1)

# valores de los tokens simples

t_TkComa = r','
t_TkPuntoYComa = r';'
t_TkParAbre = r'\('
t_TkParCierra = r'\)'
t_TkSuma = r'\+'
t_TkResta = r'-'
t_TkMult = r'\*'
t_TkDiv = r'/'
t_TkMod = r'%'
t_TkConjuncion = r'/\\'
t_TkDisyuncion = r'\\/'
t_TkNegacion = r'\^'
t_TkMenor = r'<'
t_TkMenorIgual = r'<='
t_TkMayor = r'>'
t_TkMayorIgual = r'>='
t_TkIgual = r'='
t_TkDesIgual = r'/='
t_TkHorConcat = r':'
t_TkVerConcat = r'\|'
t_TkRot = r'\$'
t_TkTras = r'\''
t_TkAsignacion = r':='

# contruir el analizador lexico
lexer=lex.lex(debug=0)
archi = sys.stdin.read()

#----------------#
# Precedencia	 #
#----------------#


precedence = (
	 ('left','TkConjuncion','TkDisyuncion'),
	 ('left','TkHorConcat','TkVerConcat'),
	 ('left','TkRot'),
	 ('right','TkTras'),
     ('left', 'TkSuma', 'TkResta'),
  	 ('left','TkMult','TkDiv','TkMod'),
  	 ('right','TkNegacion'),
  	 ('left','TkIgual','TkDesIgual')
)


#----------------#
#    impresion   #
#----------------#

class Impre:
	def __init__(self,expr1,expr2):
		self.expr1 = expr1
		self.expr2 = expr2
	def __str__(self):
		return str(self.expr1) + ';' + str(self.expr2)

class Impre_uni:
	def __init__(self,expr):
		self.expr = expr
	def __str__(self):
		return str(self.expr)

class Impre_err:
	def __init__(self,expr):
		self.expr = expr
	def __str__(self):
		temp = 'SECUENCIACION'
		for expr in self.expr:
			temp = temp + str(expr) + ';'
		temp = temp[:-1]
		return "Error: " + aux

class Impre2:
	def __init__(self,expr1,expr2):
		self.expr1 = expr1
		self.expr2 = expr2
	def __str__(self):
		return str(self.expr1) + " ; " + str(self.expr2)


class expresion : pass



class OpBin(expresion):
	def __init__(self,op1,op2):
		self.op1 = op1
		self.op2 = op2

class Suma(OpBin):
	def __str__(self):
		return "Suma(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")" 

class Resta(OpBin):
	def __str__(self):
		return "Resta(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class Mult(OpBin):
	def __str__(self):
		return "Multiplicacion(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class Div(OpBin):
	def __str__(self):
		return "Division(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class Modulo(OpBin):
	def __str__(self):
		return "Modulo(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class And(OpBin):
	def __str__(self):
		return "And(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class Or(OpBin):
	def __str__(self):
		return "Or(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class Menor(OpBin):
	def __str__(self):
		return "Menor que(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class MenorIg(OpBin):
	def __str__(self):
		return "Menor igual(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class Mayor(OpBin):
	def __str__(self):
		return "Mayor que(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class MayorIg(OpBin):
	def __str__(self):
		return "Mayor igual(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class Igual(OpBin):
	def __str__(self):
		return "Igual(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class Desigual(OpBin):
	def __str__(self):
		return "Desigual(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class ConcatVer(OpBin):
	def __str__(self):
		return "Concadenacion Vertical(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class ConcatHor(OpBin):
	def __str__(self):
		return "Concadenacion Horizontal(" + "operador izquierdo= " + str(self.op1) + " ,operador derecho= " + str(self.op2) + ")"

class OpUn(expresion):
	def __init__(self,op1):
		self.op1 = op1

class Menos(OpUn):
	def __str__(self):
		return "Negativo(" + str(self.op1) + ")"

class Nega(OpUn):
	def __str__(self):
		return "Negacion(" + str(self.op1) + ")"

class Rota(OpUn):
	def __str__(self):
		return "Rotacion(" + str(self.op1) + ")"

class Trans(OpUn):
	def __str__(self):
		return "Traspocision(" + str(self.op1) + ")"

class IfElse(expresion):
	def __init__(self,boolean,ex1,ex2):
		self.boolean = boolean
		self.ex1 = ex1
		self.ex2 = ex2

	def __str__(self):
		return "If-Else(" + "Condicion= "+ str(self.boolean) + " ,Instruccion= " + str(self.ex1) + " ,Instruccion= " + str(self.ex2) + ")"

class IfS(expresion):
	def __init__(self,boolean,ex1):
		self.boolean = boolean
		self.ex1 = ex1
	def __str__(self):
		return "If(" + "Condicion= "+ str(self.boolean) + " ,Instruccion= " + str(self.ex1) + ")"

class While(expresion):
	def __init__(self,boolean,ex1):
		self.boolean = boolean
		self.ex1 = ex1
	def __str__(self):
		return "While(" + "Condicion= "+ str(self.boolean) + " ,Instruccion= " + str(self.ex1) + ")"

class Fro(expresion):
	def __init__(self,num1,num2,ex1):
		self.num1 = num1
		self.num2 = num2
		self.ex1 = ex1
	def __str__(self):
		return "From(" + "Limite Inferior= " + str(self.num1) + " ,Limite Superior = " + str(self.num2) + " ,Instruccion" + str(self.ex1) + ")"

class With(expresion):
	def __init__(self,iden,num1,num2,ex1):
		self.iden = iden
		self.num1 = num1
		self.num2 = num2
		self.ex1= ex1
	def __str__(self):
		return "From-With(" + "Contador= " + str(self.iden) + " ,Limite Inferior = " + str(self.num1) + " ,Limite Superior= " + str(self.num2) + " ,Instruccion= " + str(self.ex1) + ")"

class Asig(expresion):
	def __init__(self,iden,ex1):
		self.iden = iden
		self.ex1 = ex1
	def __str__(self):
		return "Asignacion(" + "Variable= " + str(self.iden) + ", Expresion= " + str(self.ex1) + ")"

class Read(expresion):
	def __init__(self,iden):
		self.iden = iden
	def __str__(self):
		return "Read(" + "Variable= " + str(self.iden) + ")"

class Print(expresion):
	def __init__(self,iden):
		self.iden = iden
	def __str__(self):
		return "Print(" + "Lienzo= " + str(self.iden) + ")"


#################################################################
###                  VERIFICACION DE TIPO                     ###
#################################################################

def evaluar(arbol):
	if (isinstance(arbol, Impre)):
		aux1 = arbol.expr1
		aux2 = arbol.expr2
		if(isinstance(aux1, Impre_uni) or isinstance(aux1,Impre)):
			evaluar(aux1)
		if(isinstance(aux2,Impre) or isinstance(aux2,Impre_uni)):
			evaluar(aux2)
			
	elif(isinstance(arbol,Impre_uni)):
		aux = arbol.expr
		if(isinstance(aux,Asig)):
			aux2 = aux.ex1
			aux1 = aux.iden
			temp2 = Tipo(aux1)
			temp3 = calcularExprBin(aux2)
			if(temp2 == temp3):
				run(aux)
			else:
				print 'error de tipo {0}'.format(temp2)
		elif(isinstance(aux,IfElse)):
			aux1 = aux.boolean
			aux2 = aux.ex1
			aux3 = aux.ex2
			if(isinstance(aux1,OpBin) or isinstance(aux1,OpUn)):
				temp = calcularExprBin(aux1)
			else:
				temp = Tipo(aux1)
			if(temp == 'boolean'):
				run(aux)
			else:
				print 'error de tipo {0}'.format(temp)
		elif(isinstance(aux,IfS)):
			aux1 = aux.boolean
			aux2 = aux.ex1
			if(isinstance(aux1,OpBin) or isinstance(aux1,OpUn)):
				temp = calcularExprBin(aux1)
			else:
				temp = Tipo(aux1)
			if(temp == 'boolean'):
				run(aux)
			else:
				print 'error de tipo {0}'.format(temp)
		elif(isinstance(aux,While)):
			aux1 = aux.boolean
			aux2 = aux.ex1
			if(isinstance(aux1,OpBin) or isinstance(aux1,OpUn)):
				temp = calcularExprBin(aux1)
			else:
				temp = Tipo(aux1)
			if(temp == 'boolean'):
					run(aux)
			else:
				print 'error de tipo {0}'.format(temp)
		elif(isinstance(aux,Read)):
			temp = aux.iden
			if(tabla.has_key(temp)):
				aux1 = Tipo(temp)
				if(aux1 == 'integer'):
					run(aux)
				else:
					print 'La variable1 [{0}] debe ser de tipo entera'.format(temp)
					exit(1)
			else:
				print 'errorde sintaxis {0} no fue declarada'.format(temp)
				exit(1)
		elif(isinstance(aux,Print)):
			temp = aux.iden
			if(temp[0] != '<'):
				if(tabla.has_key(temp)):
					temp1 = Tipo(temp)
					if(temp1 == 'canvas'):
						run(aux)
					else:
						print 'La variable [{0}] debe ser de tipo canvas'.format(temp)
						exit(1)
				else:
					print 'error de sintaxis2 {0} no fue declarada'.format(temp)
					exit(1)	
			else:
				run(aux)
		elif(isinstance(aux,With)):
			temp = aux.iden
			temp2 = aux.num1
			temp3 = aux.num2
			if(tabla.has_key(temp)):
				if(Tipo(temp) == Tipo(temp2) == Tipo(temp3) == 'integer'):
					run(aux)
				elif(Tipo(temp) != 'integer'):
					print 'La variable [{0}] debe ser de tipo entera'.format(temp)
					exit(1)
				elif(Tipo(temp2) != integer):
					print 'La variable [{0}] debe ser de tipo entera'.format(temp2)
					exit(1)
				elif(Tipo(temp) != 'integer'):
					print 'La variable [{0}] debe ser de tipo entera'.format(temp3)
					exit(1)
			else:
				print 'error de sintaxis3 {0} no fue declarada'.format(p[2])
				exit(1)
		elif(isinstance(aux,Fro)):
			temp = aux.num1
			temp2 = aux.num2
			if(Tipo(temp) == Tipo(temp2) == 'integer'):
				run(aux)
			else:
				print 'Los limites deben ser de tipo integer'
		
	



def Tipo(aux):
	if(tabla.has_key(aux)):
			temp = tabla[aux]
			temp = temp[0]
			return temp	
	elif(type(aux) == int):
			temp = 'integer'
			return temp
	elif(aux == 'true' or aux == 'false'):
			return 'boolean'
	elif(aux[0] == '<'):
			return 'canvas'
	elif(not(tabla.has_key(aux))):
			print 'error de Tipo sintaxis {0} no fue declarada'.format(aux)
			exit(1)


def calcularExprBin(exp):
	if(isinstance(exp,OpBin)):
		aux = exp.op1
		aux2 = exp.op2
		if(isinstance(exp,Menor)):
			if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
				temp = calcularExprBin(aux)
			else:
				temp = Tipo(aux)

			if(isinstance(aux2,OpBin) or isinstance(aux2,OpUn)):
				temp2 = calcularExprBin(aux2)
			else:
				temp2 = Tipo(aux2)
			
			if(temp == 'integer' and temp2 == 'integer'):
				return 'boolean'
			else:
				return '1'
		elif(isinstance(exp,MenorIg)):
			if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
				temp = calcularExprBin(aux)
			else:
				temp = Tipo(aux)

			if(isinstance(aux2,OpBin) or isinstance(aux2,OpUn)):
				temp2 = calcularExprBin(aux2)
			else:
				temp2 = Tipo(aux2)
		
			if(temp == 'integer' and temp2 == 'integer'):
				return 'boolean'
			else:
				return '1'
		elif(isinstance(exp,Mayor)):
			if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
				temp = calcularExprBin(aux)
			else:
				temp = Tipo(aux)

			if(isinstance(aux2,OpBin) or isinstance(aux2,OpUn)):
				temp2 = calcularExprBin(aux2)
			else:
				temp2 = Tipo(aux2)
		
			if(temp == 'integer' and temp2 == 'integer'):
				return 'boolean'
			else:
				return '1'
		elif(isinstance(exp,MayorIg)):
			if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
				temp = calcularExprBin(aux)
			else:
				temp = Tipo(aux)

			if(isinstance(aux2,OpBin) or isinstance(aux2,OpUn)):
				temp2 = calcularExprBin(aux2)
			else:
				temp2 = Tipo(aux2)
		
			if(temp == 'integer' and temp2 == 'integer'):
				return 'boolean'
			else:
				return '1'
		elif(isinstance(exp,Igual)):
			if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
				temp = calcularExprBin(aux)
			else:
				temp = Tipo(aux)

			if(isinstance(aux2,OpBin) or isinstance(aux2,OpUn)):
				temp2 = calcularExprBin(aux2)
			else:
				temp2 = Tipo(aux2)
		
			if(temp == 'boolean' or temp2 == 'boolean'):
				return '1'
			elif(temp2 == temp):
				return 'boolean'
			else:
				return '1'
		elif(isinstance(exp,Desigual)):
			if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
				temp = calcularExprBin(aux)
			else:
				temp = Tipo(aux)

			if(isinstance(aux2,OpBin) or isinstance(aux2,OpUn)):
				temp2 = calcularExprBin(aux2)
			else:
				temp2 = Tipo(aux2)
		
			if(temp == 'boolean' or temp2 == 'boolean'):
				return '1'
			elif(temp2 == temp):
				return 'boolean'
			else:
				return '1'
		
		elif(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
			temp = calcularExprBin(aux)
		else:
			temp = Tipo(aux)

		if(isinstance(aux2,OpBin) or isinstance(aux2,OpUn)):
			temp2 = calcularExprBin(aux2)
		else:
			temp2 = Tipo(aux2)
		
		if(temp2 == temp):
			return temp
		else:
			return '1'
	
	elif(isinstance(exp,OpUn)):
		aux = exp
		if(isinstance(aux,Nega)):
				aux = aux.op1
				if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
					temp = calcularExprBin(aux)
				else:
					temp = Tipo(aux)
				if(temp == 'boolean'):
					return temp
				else:
					return '1'
		elif(isinstance(aux,Rota)):
				aux = aux.op1
				if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
					temp = calcularExprBin(aux)
				else:
					temp = Tipo(aux)
				if(temp == 'canvas'):
					return temp
				else:
					return '1'
		elif(isinstance(aux,Trans)):
				aux = aux.op1
				if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
					temp = calcularExprBin(aux)
				else:
					temp = Tipo(aux)
				if(temp == 'canvas'):
					return temp
				else:
					return '1'
		elif(isinstance(aux,Menos)):
				aux = aux.op1
				if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
					temp = calcularExprBin(aux)
				else:
					temp = Tipo(aux)
				if(temp == 'integer'):
					return temp
				else:
					return '1'
	elif(type(exp) == int):
		return 'integer'
	elif(exp == 'true' or exp == 'false'):
		return 'boolean'
	elif(exp[0] == '<'):
		return 'canvas'
	else:
		return Tipo(exp)


#################################################################
###                  FUNCIONES DE EVALUACION                  ###
#################################################################


def run(exp):
	if(isinstance(exp,OpBin)):
		a = exp.op1
		b = exp.op2
		if(isinstance(a,OpBin) or isinstance(a,OpUn)):
			f1 = run(a)
		else:
			if(tabla.has_key(a)):
				temp = tabla[a]
				if(temp[2] == ''):
					print 'Variable no inicializada {0}'.format(a)
					exit(1)
				else:
					f1 = temp[2]
			else:
				f1 = a
		if(isinstance(b,OpBin) or isinstance(b,OpUn)):
			f2 = run(b)
		else:
			if(tabla.has_key(b)):
				temp = tabla[b]
				if(temp[2] == ''):
					print 'Variable no inicializada {0}'.format(b)
					exit(1)
				else:
					f2 = temp[2]
			else:
				f2 = b
		if(isinstance(exp,Suma)):
			return eval('f1+f2')
		if(isinstance(exp,Resta)):
			return eval('f1-f2')
		if(isinstance(exp,Mult)):
			return eval('f1*f2')
		if(isinstance(exp,Modulo)):
			return eval('f1%f2')
		if(isinstance(exp,Div)):
			if(f2 == 0):
				print 'Error division por 0'
			else:
				return eval('f1/f2')
		if(isinstance(exp,And)):
			return eval('f1 and f2')
		if(isinstance(exp,Or)):
			return eval('f1 or f2')
		if(isinstance(exp,Menor)):
			return eval('f1<f2')
		if(isinstance(exp,MenorIg)):
			return eval('f1<=f2')
		if(isinstance(exp,Mayor)):
			return eval('f1>f2')
		if(isinstance(exp,MayorIg)):
			return eval('f1>=f2')
		if(isinstance(exp,Igual)):
			return eval('f1 == f2')
		if(isinstance(exp,Desigual)):
			return eval('f1 != f2')
		if(isinstance(exp,ConcatHor)):
			if(f1[0] == f2[0] == '<'):
				ret = []
				if(f1 != '<empty>'):
					ret.append(f1[1:len(f1)-1])
				else:
					pass
				if(f2 != '<empty>'):
					ret.append(f2[1:len(f2)-1])
				else:
					pass
				return ret
			elif(f1[0] == '<'):
				count = 0
				for i in f2:
					if(i == '\n'):
						count += 1
				if(count == 0):
					ret = []
					if(f1 != '<empty>'):
						ret.append(f1[1:len(f1)-1])
					else:
						pass
					for i in f2:
						ret.append(i)
					return ret
				else:
					print 'Dimension2 de lienzos diferentes'
					exit(1)
			elif(f2[0] == '<'):
				count = 0
				for i in f1:
					if(i == '\n'):
						count += 1
				if(count == 0):
					ret = []
					for i in f1:
						ret.append(i)
					if(f2 != '<empty>'):
						ret.append(f2[1:len(f2)-1])
					else:
						pass
					return ret
				else:
					print 'Dimension1 de lienzos diferentes'
					exit(1)
			else:
				count1 = 0
				count2 = 0
				for i in f1:
					if(i == '\n'):
						count1 += 1
				for i in f2:
					if(i == '\n'):
						count2 += 1
				if(count1 == count2):
					ret = []
					i = 0
					j = 0
					while (i != len(f1) or (j != len(f2))):
						if(i != len(f1)):
							if((f1[i] != '\n')):
								ret.append(f1[i])
								i += 1
							elif(f1[i] == '\n'):
								if(j != len(f2)):
									if(f2[j] != '\n'):
										ret.append(f2[j])
										j += 1
									elif(f2[j] == '\n'):
										ret.append('\n')
										i += 1
										j += 1
						else:
							ret.append(f2[j])
							j += 1
					return ret
							
				else:
					print 'Dimension3 de lienzos diferentes'
					exit(1)
		if(isinstance(exp,ConcatVer)):
			if(f1[0] == f2[0] == '<'):
				ret = []
				if(f1 != '<empty>'):
					ret.append(f1[1:len(f1)-1])
					ret.append('\n')
				else:
					pass
				if(f2 != '<empty>'):
					ret.append(f2[1:len(f2)-1])
				else:
					pass
				return ret
			elif(f1[0] == '<'):
				ret = []
				count = 0
				i = 0
				while(f2[i] != '\n'):
					count += 1
					i += 1
					if(i == len(f2)):
						break
				if(count == 1 or f1 == '<empty>'):
					if(f1 != '<empty>'):
						ret.append(f1[1:len(f1)-1])
						ret.append('\n')
					else:
						pass
					for i in f2:
						ret.append(i)
					return ret
				else:
					print 'Dimension4 de lienzos diferentes'
					exit(1)
			elif(f2[0] == '<'):
				ret = []
				i = 0
				count = 0
				while(f1[i] != '\n'):
					count += 1
					i += 1
					if(i == len(f1)):
						break
				if(count == 1 or f2 == '<empty>'):
					for i in f1:
						ret.append(i)
					ret.append('\n')
					if(f2 != '<empty>'):
						ret.append(f2[1:len(f2)-1])
					else:
						pass
					return ret
				else:
					print 'Dimension de lienzos diferentes'
					exit(1)
			else:
				ret = []
				count1 = 0
				count2 = 0
				i = 0
				while(f1[i] != '\n'):
					count1 += 1
					i += 1
					if(i == len(f1)):
						break
				i = 0
				while(f2[i] != '\n'):
					count2 +=1
					i += 1
					if(i == len(f2)):
						break
				if(count1 == count2):
					for i in f1:
						ret.append(i)
					ret.append('\n')
					for i in f2:
						ret.append(i)
					return ret
				else:
					print 'Dimension de lienzos diferentes'
					exit(1)
	elif(isinstance(exp,OpUn)):
		if(isinstance(exp,Menos)):
			a = exp.op1
			if(isinstance(a,OpBin) or isinstance(a,OpUn)):
				f1 = run(a)
			else:
				if(tabla.has_key(a)):
					temp = tabla[a]
					if(temp[2] == ''):
						print 'Variable no inicializada {0}'.format(a)
						exit(1)
					else:
						f1 = temp[2]
				else:
					f1 = a
			return eval('(-1) * f1')
		if(isinstance(exp,Nega)):
			a = exp.op1
			if(isinstance(a,OpBin) or isinstance(a,OpUn)):
				f1 = run(a)
				if(f1 == 'false'):
					f1 = False
				else:
					f1 = True
			else:
				if(tabla.has_key(a)):
					temp = tabla[a]
					if(temp[2] == ''):
						print 'Variable no inicializada {0}'.format(a)
						exit(1)
					else:
						f1 = temp[2]
				else:
					if(a == 'false'):
						f1 = False
					else:
						f1 = True
			return eval('not f1')
		if(isinstance(exp,Trans)):
			aux = exp.op1
			if(isinstance(aux,OpBin) or isinstance(aux,OpUn)):
				f1 = run(aux)
			else:
				if(tabla.has_key(aux)):
					temp = tabla[aux]
					f1 = temp[2]
				else:
					f1 = aux
					return f1
			res = []
			fin = []
			prb = []
			for i in f1:
				if(i == '\n'):
					res.append(prb)
					prb = []
				else:
					prb.append(i)
			res.append(prb)
			prb = []
			for i in range(len(res[0])):
				prb.append([])
			for i in range(len(prb)):
				for j in range(len(res)):
					prb[i].append(',')
			for i in range(len(res)):
				for j in range(len(res[0])):
					prb[j][i] = res[i][j]
			for i in range(len(prb)):
				for j in range(len(prb[i])):
					fin.append(prb[i][j])
				fin.append('\n')
			return fin
			
				
		if(isinstance(exp,Rota)):
			pass
	elif(isinstance(exp,Asig)):
		temp = exp.iden
		temp2 = exp.ex1
		temp3 = run(temp2)
		temp4 = tabla[temp]
		temp4[2] = temp3
	elif(isinstance(exp,IfElse)):
		temp = exp.boolean
		temp1 = exp.ex1
		temp2 = exp.ex2
		if(isinstance(temp,OpBin) or isinstance(temp,OpUn)):
			temp3 = calcularExprBin(temp)
		else:
			temp3 = Tipo(temp)
		if(temp3 == 'boolean'):
			temp3 = run(temp)
			if(temp3 == 'true' or temp3 == True):
				run(temp1)
			else:
				run(temp2)
		else:
			print 'La variable {0} debe ser de tipo booleano'.format(temp)
			exit(1)
	elif(isinstance(exp,IfS)):
		temp1 = exp.boolean
		temp2 = exp.ex1
		if(isinstance(temp1,OpBin) or isinstance(temp1,OpUn)):
			temp = calcularExprBin(temp1)
		else:
			temp = Tipo(temp1)
		if(temp == 'boolean'):
			temp = run(temp1)
			if(temp == 'true' or temp == True):
				run(temp2)
		else:
			print 'La variable {0} debe ser de tipo booleano'.format(temp)
			exit(1)
	elif(isinstance(exp,With)):
		iden = exp.iden
		temp5 = exp.num1
		temp6 = exp.num2
		temp4 = exp.ex1
		flag = 0
		if(tabla.has_key(iden)):
			guardar = tabla[iden]
			guardar2 = guardar[0]
			guardar = guardar[2]
			flag = 1
		tabla[iden] = ['integer',0,'']
		if(Tipo(iden) == Tipo(temp6) == Tipo(temp5) == 'integer'):
			if(tabla.has_key(temp5)):
				temp1 = tabla[temp5]
				aux = temp1[2]
			else:
				aux = temp5
			if(tabla.has_key(temp6)):
				temp2 = tabla[temp6]
				aux2 = temp2[2]
			else:
				aux2 = temp6
			temp = tabla[iden]
			if(type(temp5) != int and type(temp6) != int):
				if(aux < aux2):
					temp[2] = aux
					while(aux != (aux2+1)):
						run(temp4)
						temp[2] = temp[2] + 1
						aux = temp[2]
				else:
					print 'Los limites no concuerdan'
			elif(type(temp6) != int):		
				if(aux < aux2):
					temp[2] = aux
					while(aux != (aux2+1)):
						run(temp4)
						temp[2] = temp[2] + 1
						aux = temp[2]
				else:
					print 'Los limites no concuerdan'
			elif(type(temp5) != int):		
				if(aux < aux2):
					temp[2] = aux
					while(aux != (aux2+1)):
						run(temp4)
						temp[2] = temp[2] + 1
						aux = temp[2]
				else:
					print 'Los limites no concuerdan'
			elif(aux < aux2):
				temp[2] = aux
				while(aux != (aux2+1)):
					run(temp4)
					temp[2] = temp[2] + 1
					aux = temp[2]
			else:
					print 'Los limites no concuerdan'
					exit(1)
			if(flag == 1):
				guardar3 = tabla[iden]
				guardar3[2] = guardar
				guardar3[0] = guardar2
				tabla[iden] = guardar3
			else:
				del tabla[iden]
			
	elif(isinstance(exp,Fro)):
		temp2 = exp.num1
		temp3 = exp.num2
		temp4 = exp.ex1
		if(Tipo(temp2) == Tipo(temp3) == 'integer'):
			if(tabla.has_key(temp2)):
				temp = tabla[temp2]
				aux = temp[2]
			else:
				aux = temp2
			if(tabla.has_key(temp3)):
				temp = tabla[temp3]
				aux2 = temp[2]
			else:
				aux2 = temp3
			if(type(temp3) != int and type(temp2) != int):
				if(aux < aux2):
					while(aux != (aux2 + 1)):
						run(temp4)
						aux = aux + 1
				else:
					print 'Los limites no concuerdan'
			elif(type(temp3) != int):
				temp = tabla[temp3]		
				if(aux < aux2):
					while(aux != (aux2 + 1)):
						run(temp4)
						aux = aux + 1
				else:
					print 'Los limites no concuerdan'
			elif(type(temp2) != int):
				temp = tabla[temp2]		
				if(aux < aux2):
					while(aux != (aux2 + 1)):
						run(temp4)
						aux = aux + 1
				else:
					print 'Los limites no concuerdan'
			elif(aux < aux2):
				while(aux != (aux2+1)):
					run(temp4)
					aux = aux + 1
			else:
					print 'Los limites no concuerdan'
	elif(isinstance(exp,While)):
		aux1 = exp.boolean
		aux2 = exp.ex1
		if(isinstance(aux1,OpBin) or isinstance(aux1,OpUn)):
			aux = calcularExprBin(aux1)
		else:
			aux = Tipo(aux1)
		if(aux == 'boolean'):
			while(run(aux1) == 'true' or run(aux1) == True):
				run(aux2)
		else:
			print 'La variable {0} debe ser de tipo booleano'.format(aux)
			exit(1)
			
########################################################
	elif(isinstance(exp,Read)):
		aux = exp.iden
		temp = tabla[aux]
		temp3 = raw_input(' ')
		if(type(temp3) == int):
			temp[2] = temp3
		else:
			print 'La entrada es de enteros'
			exit(1)
	elif(isinstance(exp,Print)):
		aux = exp.iden
		temp = run(aux)
		if(temp[0] == '<'):
			if(temp != '<empty>'):
				print temp[1:len(temp)-1]
			else:
				print 
		else:
			for i in temp:
				sys.stdout.write(i)
			print 
		
#########################################################
			
	elif(isinstance(exp,Impre)):
		a = exp.expr1
		b = exp.expr2
		run(a)
		run(b)
	elif(isinstance(exp,Impre_uni)):
		a = exp.expr
		run(a)
	else:
		if(tabla.has_key(exp)):
			temp = tabla[exp]
			if(temp[2] == ''):
				print 'Variable {0} no inicializada'.format(exp)
				exit(1)
			else:
				if(temp[0] != 'canvas'):
					return temp[2]
				else:
					return temp[2]
		else:
			return exp
			




################################################################	
###                       ARBOL SINTACTICO                   ###
################################################################


tabla = {}
contador = 0
temp = []

def p_expr(p):
	''' expr : 	TkUsing Declar TkBegin expr TkEnd
				| TkBegin expr TkEnd
				| expr TkPuntoYComa expr 
				| instr '''
	global contador
	global temp
	if len(p) == 4:
		if(p[2] == ';'):
			p[0] = Impre(p[1],p[3])
		else:
			p[0] = p[2]
	elif(len(p) == 6):
		temp = []
		contador += 1
		p[0] = p[4]
		for i in tabla:
			count = contador
			aux = tabla[i]
			aux2 = aux[-1]
			while(type(aux2) == list):
				if(type(aux[1]) == int):
					aux = aux2
					aux2 = aux[-1]
				else:
					aux[1] = count					
					aux = aux2
					aux2 = aux[-1]
	else:
		p[0] = Impre_uni(p[1])

def p_Declar(p):
	''' Declar : Declar TkComa TkIdent TkOfType Tipo
				  | Declar TkComa TkIdent
				  | TkIdent TkOfType Tipo
				  | Declar TkPuntoYComa Declar 
				  | TkIdent '''
	global temp
	global contador
	cont = 0
	if(len(p) == 4):

		if(p[2] == ','):
			temp.append(p[3])
			p[0] = p[1]
		elif(p[2] == ';'):
			temp.append(p[1])
			temp.append(p[3])
		else:
			if(tabla.has_key(p[1])):
					aux = tabla[p[1]]
					aux2 = aux[-1]
					while(type(aux2) == list):
						aux = aux2
						aux2 = aux[-1]
					if(aux[1] == contador):
						print 'variable repetida {0}'.format(p[1])
						exit(-1)
					else:
						aux3 = [p[3],contador,'']
						aux.append(aux3)
			else:
				lista = [p[3],contador,'']
				tabla[p[1]] = lista
			p[0] = tabla
	elif(len(p) == 6):
		temp.append(p[3])
		temp.append(p[1])
		for i in temp:
			if(tabla.has_key(i)):
				aux = tabla[i]
				aux2 = aux[-1]
				while(type(aux2) == list):
					aux = aux2
					aux2 = aux[-1]
				if(aux[1] == contador):
					print 'variable repetida {0}'.format(i)
					exit(1)
				else:
					aux3 = [p[5],contador,'']
					aux.append(aux3)
			else:
				lista = [p[5],contador,'']
				tabla[i] = lista
			temp = []

	else:
		if(tabla.has_key(p[1])):
				aux = tabla[p[1]]
				aux2 = aux[-1]
				while(type(aux2) == list):
					aux = aux2
					aux2 = aux[-1]
				if(aux[1] == contador):
					print 'variable2 repetida {0}'.format(p[1])
					exit(1)
				else:
					aux3 = [p[5],contador,'']
					aux.append(aux3)
		else:
					p[0]=p[1]
def p_Tipo(p):
	''' Tipo : TkInteger
				| TkBoolean
				| TkCanvas '''
	p[0] = p[1]

def p_instr(p):
	'''instr : TkIdent TkAsignacion booleana
		 	   | TkIf booleana TkThen expr TkElse expr TkDone
		 	   | TkIf booleana TkThen expr TkDone
		 	   | TkWhile booleana TkRepeat expr TkDone
		 	   | TkWith TkIdent TkFrom arit TkTo arit TkRepeat expr TkDone
		 	   | TkFrom arit TkTo arit TkRepeat expr TkDone 
		 	   | TkPrint TkIdent
		 	   | TkPrint TkLienzo
		 	   | TkRead TkIdent  '''

	if (len(p)== 4):
	    if (p[2] == ':='):
	    	if(tabla.has_key(p[1])):
	    		p[0] = Asig(p[1] , p[3])
	    	else:
	    		print 'errorde sintaxis {0} no fue declarada'.format(p[1])
	    		exit(1)	
	elif(len(p) == 8):
	    if(p[1] == 'if'):
	    	p[0] = IfElse(p[2],p[4],p[6])
	    if(p[1] =='from'):
	    	p[0] = Fro(p[2],p[4],p[6])	
	elif(len(p) == 6):
	    if(p[1] == 'while'):
	    	p[0] = While( p[2] , p[4])
	    elif(p[1] == 'if'):
	    	p[0] = IfS(p[2],p[4])
	elif(len(p) == 10 ):
			p[0] = With(p[2],p[4],p[6],p[8])
	elif(len(p) == 3):
		if(p[1] == 'read'):
			p[0] = Read(p[2])	
		else:	
			p[0] = Print(p[2])


def p_arit(p):
	''' arit : arit operatorA arit
		 		| TkResta arit
		 		| TkParAbre arit TkParCierra
		 		| TkNum
		 		| TkIdent '''

	if(len(p) == 4):
		if(p[2] == '+'):
			p[0] = Suma(p[1],p[3])
		if(p[2] == '-'):
			p[0] = Resta(p[1],p[3])
		if(p[2] == '*'):
			p[0] = Mult(p[1],p[3])
		if(p[2] == '/'):
			p[0] = Div(p[1],p[3])
		if(p[2] == '%'): 
			p[0] = Modulo(p[1],p[3])
		if p[1] == '(':
			if p[3] == ')':
				p[0] = p[2] 
	elif(len(p) == 3):
		p[0] = Menos(p[2])
	else:
		p[0] = p[1]


def p_booleana(p):
	''' booleana : booleana operatorB booleana
		    		 | TkParAbre booleana TkParCierra
		    		 | TkTrue
		    		 | TkFalse
				 	 | booleana TkNegacion
				 	 | arit
				 	 | lienzo '''
#| TkNegacion booleana

	if(len(p) == 4):
		if(p[2] == '/\\'):
			p[0] = And(p[1],p[3])
		if(p[2] == '\\/'):
			p[0] = Or(p[1],p[3])
		if(p[2] == '<'):
			p[0] = Menor(p[1], p[3])
		if(p[2] =='<='):
			p[0] = MenorIg(p[1],p[3])
		if(p[2] == '>'):
			p[0] = Mayor(p[1],p[3])
		if(p[2] == '>='):
			p[0] = MayorIg(p[1],p[3])
		if(p[2] == '='):
			p[0] = Igual(p[1],p[3])
		if(p[2] == '/='):
			p[0] = Desigual(p[1],p[3])
		if p[1] == '(':
			if p[3] == ')':
				p[0] = p[2]
	elif(len(p) == 3):
		p[0] = Nega(p[1])
	else:
		if(isinstance(p[1],OpBin)):
			p[0] = p[1]
		elif(isinstance(p[1],OpUn)):
			p[0] = p[1]
		elif(type(p[1]) == int):
			p[0] = p[1]
		elif(p[1] != 'true' and p[1] != 'false'):
			if(tabla.has_key(p[1])):
					p[0] = p[1]
			elif(p[1][0] == '<'):
					p[0] = p[1]
			else:
				print 'errorde sintaxis {0} no1 fue declarada'.format(p[1])
				exit(1)
		else:
			p[0] = p[1]

def p_lienzo(p):
	''' lienzo : lienzo operatorL lienzo 
		   	  | TkParAbre lienzo TkParCierra
		   	  | TkRot lienzo 
		   	  | lienzo TkTras 
		   	  | TkLienzo
		   	  | arit '''

	if len(p) == 4:
		if p[2] == ':':
			p[0] = ConcatHor(p[1],p[3])
		if p[2] == '|':
			p[0] = ConcatVer(p[1],p[3])
		if p[1] == '(':
			if p[3] == ')':
				p[0] =  p[2]
	elif (len(p)==3):
		if(p[2]=='\''):
			p[0]=Trans(p[1])
		else:		
			p[0]=Rota(p[2])

	else:
		if(p[1][0] != '<'):
				if(tabla.has_key(p[1])):
					p[0] = p[1]
				else:
					print 'errorde sintaxis {0} no fue declarada'.format(p[1])
					exit(1)
		p[0] = p[1]

def p_operatorA(p):
	''' operatorA : TkSuma
					  | TkResta
					  | TkMult
					  | TkDiv
					  | TkMod '''
	p[0] = p[1]

def p_operatorB(p):
	''' operatorB : TkMenor
					  | TkMenorIgual
					  | TkMayor
					  | TkMayorIgual
					  | TkIgual
					  | TkDesIgual 
					  | TkConjuncion
					  | TkDisyuncion '''
	p[0] = p[1]

def p_operatorL(p):
	''' operatorL : TkHorConcat
					  | TkVerConcat '''
	p[0] = p[1] 			

def p_error(p):
	print "Error de sintaxis " + p.type +" " +  p.value
	exit(1)

parser = yacc.yacc()
arbol = parser.parse(archi)
evaluar(arbol)
#print tabla
#print arbol


