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
   #print(self.__dict__.items())
   for attr, value in self.__dict__.items():
     v = str(attr) + ':' + str(value)
     output += v + '\n'

     #for x in self.parametros:
     #  output += str(x) + '\n'  
     #  for y in self.parametros[x]:
     #    name = '  ' + str( y )
     #    valor = ': ' + str( self.parametros[x][y] ) 
     #    output += name + valor + '\n'  

   return output 

tt = Track(
  track['parametros'],
  track['unidades'],
  track['forma'],
)
print(tt)


""" TODO
[ ] Agregar herencia entre unidades.
[ ] func/@property: Secuenciar unidades.
[ ] Punteros a partir de unidades contendoras de punteros.
[ ] Que las escructuras levanten params por defencto .
[ ] Que cada unidad pueda sobreescribir sus parametros.
[ ] proper eval() https://docs.python.org/3/library/ast.html 
"""
"""
Cada unidad tiene o parametros propios o parametros 
que hereda o de los params generales o de otra unidad si es 
es "hija" lo cual lo indica el prefijo "^"
"""
"""
El secuencia de indices que define el largo del loop es el mas largo
"""
