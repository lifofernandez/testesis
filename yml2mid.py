#!/usr/bin/env python3.7

import yaml
from dataclasses import dataclass

data = open( "track.yml", 'r' )
track = yaml.load( data )

@dataclass
class Track:
  parametros: dict
  unidades: dict
  forma: dict

  def __str__( self ):
    output = '' 
    for x in self.parametros:
      output += str(x) + '\n'  
      for y in self.parametros[x]:
        name = '  ' + str( y )
        valu = ': ' + str( self.parametros[x][y] ) 
        output += name + valu + '\n'  
    return output 

  @property
  def alturas( self ):
    """
    alturas son el resultado de combinar 
    propiedades adentro del parametro altura
    """
    #trasponer = octavar + self.parametros['altura']['transporte'] 
    evaluado =  evaluar( self.parametros['altura']['set'] ) 
    return evaluado 


  @property
  def secuencia( self ):
      return secuenciar( self.forma, self.unidades )



def secuenciar( forma, unidades ):
  """
  1ro = evaluar strings que no sean nobres de unidad 
  2do = remplazar string por la lista/unidad que representa
  3ro = aplanar resultado

  numero = puntero, string = unidad o rutina
  ¿if string && is not 'otra unidad' then eval?
  ¿if string 'otra unidad' then read?
  ¿eval resultado == numeros return punteros?
  ¿como saber si es micro? minusculas? 
  ¿importa si son micro? 
  ¿si es lista de numero es micro, o no?
  ¿si son numeros son micro?
  micro:
  Args: lista de unidades a aplanar, paleta de unidades
  """
  output = [] 
  for item in forma:
    #if ( isinstance( item, int ) ):
    if type( item ) is int or type( item ) is float:
      puntero = item 
      output.append( puntero )
    elif ( isinstance( item, list) ):
      unidad = item
      output += secuenciar( unidad , unidades ) 
    elif isinstance( item, str ) :
       if item in unidades:
         unidad = unidades[ item ] 
         output += secuenciar( unidad , unidades ) 
       else:
         evaluado = evaluar( item ) 
         output += secuenciar( evaluado , unidades ) 
  return output 

def evaluar(i):
  if type( i ) is int or type( i ) is float:
      return i
  #if type( i ) is str:
  if ( isinstance( i,str) ):
    o = eval( i )
  elif type( i ) is list: 
    o = [ evaluar( e ) for e in i ]
  else:
    return False
  return o

"""
'https://stackoverflow.com/questions/2357230'
for sublist in l:
    for item in sublist:
        flat_list.append(item)
"""

""" 
aplanar 2 niveles de lista 
"""
aplanar = lambda l: [item for sublist in l for item in sublist]

""" 
aplana 3 niveles de lista 
"""
def aplana(l):
  o = []
  if type( l ) is list: 
    for e in l:
      e = aplana(e)
      if type( e ) is list: 
        for i in e:
          i = aplana(i)
          o = o + [i]
      else:
        o = o + [e]
  else:
    return l
  return o

melodia = Track( 
  track['parametros'],
  track['unidades'],
  track['forma'],
)

#print(melodia)
## en realidad melida.motivo['a'].alturas
#print(melodia.alturas)
## melodia.secuencia
## ¿sería melida.motivo['a'].secuencia ?
#
#print(melodia.secuencia)

lolol = [
    2,
    [
      1,
      [8,88] *2 ,
      2,
      3
    ],
    [4,5,6], 
    [7] +[1,3,5], 
    [8,9] * 3,
    'range(0,11,2)',
    ['range(0,7,2)',33]*2
  ] * 9
aplanado = aplana( lolol ) 
evaluado = evaluar(lolol) 

print(aplanado )
print(aplanado[-2])
print(evaluado)


""" TODO
[-] func/@property: Secuenciar unidades.
[ ] Punteros a partir de unidades contendoras de punteros.
[ ] Que las escructuras levanten params por defencto .
[ ] Que cada unidad pueda sobreescribir sus parametros.
[ ] Agregar herencia entre unidades.
[ ] proper eval() https://docs.python.org/3/library/ast.html 
"""
"""
cada unidad tiene o parametros propios o parametros 
que hereda o de los params generales o de otra unidad si es 
es "hija" lo cual lo indica el prefijo "^"
"""
