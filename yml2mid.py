#!/usr/bin/env python3.7

import yaml
import weakref

import pprint
#from dataclasses import dataclass

data = open( "track.yml", 'r' )
track_file = yaml.load( data )
# esto tiene que ser de cada track ??
sufijo_prima = track_file['PRIMA']

#@dataclass
class Track:
  cantidad = 0 
 
  def __init__( 
    self,
    default,
    originales,
    macroforma,
  ):
    self.default    = default
    self.originales = originales 
    self.macroforma = macroforma
    self.secuencia = self.secuenciar()
    Track.cantidad += 1

  def __str__( self ):
    o = '' 
    for attr, value in self.__dict__.items():
      l = str(attr) + ':' + str(value)
      o += l + '\n'
    return o

  @property
  def unidades( self ):
    # pasar a init?
    UNIDADES = {} 
    for unidad in self.originales:
      unidad_objeto = Unidad( 
        unidad, 
        self.originales[ unidad ], 
        self.default,
        self
      )
      #print( unidad_objeto)
      #if( unidad_objeto.apellido):
      #  print(unidad_objeto.apellido)
      #  print(unidad_objeto.herencia)
      #  print(unidad_objeto.sucesion)
      #print(unidad_objeto.parametros)
      #unidad_objeto.mostrar_cantidad()

      UNIDADES[ unidad ] =  unidad_objeto 
    return UNIDADES

  def secuenciar( 
    self,
    forma = None,
    nivel = 0,
    PASOS = [],
    pisar = {} 
  ):
    forma = forma if forma is not None else self.macroforma
    paleta = self.unidades
    nivel += 1
    for u in forma:  
      # print( '-' * ( nivel - 1 )+ str( u ) )
      if u in paleta:
        uo = paleta[ u ]
        # mix propiedades con unidad referente
        instancia = { 
          **uo.propiedades,
          **pisar
        }
        if uo.unidades:
          us = uo.unidades
          self.secuenciar( us, nivel, PASOS, instancia  ) 
        else: # solo unidades basicas se puede secuenciar 
          print( uo, instancia )

          #calt = len( parametros['alturas'] )
          #cdur = len( parametros['duraciones'] )
          #cdin = len( parametros['dinamicas'] )
          #pasos = max(
          #  calt,
          #  cdin,
          #  cdur,
          #)
          ## Combinacion parametros: altura, duracion, dinamica, etc
          #for paso in range( pasos ):
          #  alt = parametros['alturas'][paso % calt ]
          #  # falta combinar altura con set  intervalos
          #  dur = parametros['duraciones'][paso % cdur ]
          #  din = parametros['dinamicas'][paso % cdin ]
          #  print(
          #    'evento',
          #    paso,'\t',
          #    alt,'\t',
          #    dur,'\t',
          #    din,'\t',
          #  )
          PASOS += [ u ]
    return PASOS
    
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
    self.track = weakref.ref( track )
    Unidad.cantidad += 1
    Unidad.default = default

  def __str__( self ):
    return self.nombre

  def mostrar_cantidad( self ):
    print( "Cantidad de Unidades: %d" % Unidad.cantidad )

  @property # presindible, sin uso por fuera
  def es_hijo( self ):
    return self.nombre.endswith( sufijo_prima )

  @property # presindible
  def apellido( self ):
    if self.es_hijo:
      # obtener nombre padre
      return self.nombre[0:-1]

  @property # presindible
  def herencia( self ):
    if self.apellido:
      # track() weakref track 
      herencia = self.track().originales[ self.apellido ]
      return herencia 

  @property # presindible
  def sucesion( self ):
    if self.herencia:
      # mix dicts  
      o = { **self.herencia, **self.original }
      return o

  @property 
  def propiedades( self ):
    # sucesion y/o original
    o = self.original
    if self.sucesion:
      o = { **self.sucesion, **self.original }
    return o

  @property 
  def parametros( self ):
    o = { **Unidad.default, **self.propiedades }
    return o

  #Unidad de Unidades
  @property
  def unidades( self ):
    if 'unidades' in self.parametros:
      return self.parametros['unidades']
      

t = Track(
  track_file['default'],
  track_file['unidades'],
  track_file['macroforma'],
)

#para evitar tener que ejecutar secuenciar, hay quie pasar esa func a init
#secuencia = t.secuenciar()
print(t.secuencia)



""" TODO
[x] Agregar herencia entre unidades prima y padre.
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
