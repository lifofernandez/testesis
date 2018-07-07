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
   for attr, value in self.__dict__.items():
     v = str(attr) + ':' + str(value)
     output += v + '\n'
   return output 

  def heredar( self ):
    for unidad in self.unidades:
      unidad_objeto = Unidad( unidad, self.unidades[unidad])
      print( unidad_objeto )
      unidad_objeto.mostrar_cantidad()

      # output += str(x) + '\n'  
      # for y in self.parametros[x]:
      #if(unidad[-1] == '^'):
      #   print(unidad+':HIJAA')
      #if 'unidades' in self.unidades[unidad]:
      #   print( unidad + ':UoU' )
      #else : 
      #   print( unidad + ':Unidad Basica' )
      ##if( isinstance( self.unidades[unidad], dict) ):
      ##  print( 'dict:'+ str(unidad ))
      ##  #print(unidad[-1] ) 
      ##elif( isinstance( self.unidades[unidad],list) ):
      ##  print( 'list:'+str(unidad))
    return 'e'

class Unidad:
  cantidad = 0
  def __init__( self, nombre, unidad_original ):
    self.nombre = nombre 
    Unidad.cantidad += 1

  def __str__( self ):
   return self.nombre

  def mostrar_cantidad( self):
      print("Cantidad de Unidades: %d" % Unidad.cantidad)

    
"""
clase para pasar las unidades de cada track
metodos: es_hijo, heredar/suceder, init(levantar defaults y override con propios),
es UoU o Unidad Bassica,
¿primero se prosesan unidades basicas, luego UoU?
¿primero hereda, despues completa con parametros generales?
   def es_hijo?
"""

tt = Track(
  track['modelo'],
  track['unidades'],
  track['forma'],
)
print(tt)
tt.heredar()


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
