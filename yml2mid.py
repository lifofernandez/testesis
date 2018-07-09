#!/usr/bin/env python3.7

import yaml
import weakref
from dataclasses import dataclass

data = open( "track.yml", 'r' )
track_file = yaml.load( data )
# esto tiene que ser de cada track ??
sufijo_prima = track_file['PRIMA']

@dataclass
class Track:
  default: dict
  unidades: dict
  forma: dict

  def __str__( self ):
   o = '' 
   for attr, value in self.__dict__.items():
     l = str(attr) + ':' + str(value)
     o += l + '\n'
   return o

  # pasar a init
  def cargar_unidades( self ):
    for unidad in self.unidades:
      unidad_objeto = Unidad( 
        unidad, 
        self.unidades[unidad], 
        self.default,
        self
      )
      print( unidad_objeto)
      if( unidad_objeto.apellido):
        print(unidad_objeto.apellido)
        print(unidad_objeto.herencia)
        print(unidad_objeto.sucesion)
      #unidad_objeto.mostrar_cantidad()

    return 'e'

    
"""
clase para pasar las unidades de cada track
metodos: es_hijo, heredar/suceder, init(levantar defaults y override con propios),
es UoU o Unidad Bassica,
¿primero se prosesan unidades basicas, luego UoU?
¿primero hereda, despues completa con parametros generales?
   def es_hijo?
   PRIMERO HEREDA ASI DESPUES PPLANCHA DEFAULTS
   SINO PLANCHA DEDEI DEFAULS Y DESPUES PLANCHA PADRE
"""
class Unidad:
  cantidad = 0
  def __init__( 
      self,
      nombre,
      cruda,
      default,
      track
    ):
    self.nombre = nombre 
    self.original = cruda
    self.track = weakref.ref(track)
    Unidad.cantidad += 1
    #print(Unidad)

  def __str__( self ):
    return self.nombre

  def mostrar_cantidad( self ):
    print("Cantidad de Unidades: %d" % Unidad.cantidad)

  @property
  def es_hijo( self ):
    return self.nombre.endswith( sufijo_prima )

  @property
  def apellido( self ):
    if self.es_hijo:
      # obtener nombre padre
      return self.nombre[0:-1]

  @property
  def herencia( self ):
    if self.apellido:
      # track() invoca a la ref de track 
      herencia = self.track().unidades[ self.apellido ]
      return herencia 

  @property
  def sucesion( self ):
    if self.herencia:
      # mix dicts  
      o = { **self.herencia, **self.original }
      return o

tt = Track(
  track_file['default'],
  track_file['unidades'],
  track_file['forma'],
)
print(tt)
tt.cargar_unidades()


""" TODO
[-] Agregar herencia entre unidades prima y padre.
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
