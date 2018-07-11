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
  originales: dict
  forma: dict

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
        self.originales[unidad], 
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

      UNIDADES[unidad] =  unidad_objeto 
    return UNIDADES

  @property
  def secuencia( self ):

    for U in self.forma:
      print(U)

    for u in self.unidades:  
      unidad = self.unidades[ u ]

      if unidad.unidades:
        print( unidad )
        print( unidad.parametros )

        for r in unidad.unidades:
          referida = self.unidades[ r ]
          print( '-', referida )
          referente = unidad.parametros 
          referente.pop( 'unidades', None )
          resultado = { **referida.parametros, **referente} 

          if referida.unidades:
            for rr in referida.unidades:
              refereferida = self.unidades[ rr ]
              print( '--', refereferida )
              #refereferente = referida.parametros 
              refereferente = resultado
              refereferente.pop( 'unidades', None )
              reresultado = { **refereferida.parametros, **refereferente} 

      #if not unidad.unidades:
      #else:
      #  parametros = unidad.parametros

      #  cantidad_alturas    = len( parametros['alturas'] )
      #  cantidad_duraciones = len( parametros['duraciones'] )
      #  cantidad_dinamicas  = len( parametros['dinamicas'] )
      #  pasos = max(
      #    cantidad_alturas,
      #    cantidad_duraciones,
      #    cantidad_dinamicas,
      #  )

      #  # Combinacion parametros: altura, duracion, dinamica, etc
      #  for paso in range( pasos ):
      #    altura = parametros['alturas'][paso % cantidad_alturas]
      #    # combinar con intervalos
      #    duracion = parametros['duraciones'][paso % cantidad_duraciones]
      #    dinamica = parametros['dinamicas'][paso % cantidad_dinamicas]
      #    print(
      #      'evento',
      #      paso,'\t',
      #      altura,'\t',
      #      duracion,'\t',
      #      dinamica,'\t',
      #    )
    return 'secuencia'

  def eventos( self ):
    # Secuencia de eventos 
    return 'eventos'
    
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
    Unidad.default = default

  def __str__( self ):
    return self.nombre

  def mostrar_cantidad( self ):
    print("Cantidad de Unidades: %d" % Unidad.cantidad)

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
      # track() invoca a la ref de track 
      herencia = self.track().originales[ self.apellido ]
      return herencia 

  @property # presindible
  def sucesion( self ):
    if self.herencia:
      # mix dicts  
      o = { **self.herencia, **self.original }
      return o

  @property 
  def parametros( self ):
    if self.sucesion:
      o = { **Unidad.default, **self.sucesion }
    else:
      o = { **Unidad.default, **self.original }
    return o

  #Unidad de Unidades
  @property
  def unidades( self ):
    if 'unidades' in self.parametros:
      return self.parametros['unidades']
      

t = Track(
  track_file['default'],
  track_file['unidades'],
  track_file['forma'],
)
#print(t)
#for u in t.unidades:
#  print(u)

o = t.secuencia
#for s in t.eventos:
#  print(s)


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
