#!/usr/bin/env python3.7

import yaml
import weakref

from music21 import *
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
      l = str( attr ) + ':' + str( value )
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
      UNIDADES[ unidad ] =  unidad_objeto 
    return UNIDADES

  def secuenciar( 
    self,
    forma = None,
    nivel = 0,
    secuencia = [],
    pisar = {} 
  ):
    forma = forma if forma is not None else self.macroforma
    paleta = self.unidades
    nivel += 1
    for u in forma:  
      # print( '-' * ( nivel - 1 )+ str( u ) )
      if u in paleta:
        uo = paleta[ u ]
        # Mix propiedades con unidad referente
        referente = { 
          **uo.propiedades,
          **pisar
        }
        if uo.unidades:
          us = uo.unidades
          self.secuenciar( us, nivel, secuencia, referente) 
        else: 
          # solo unidades basicas se puede secuenciar 
          resultado = {
            **uo.parametros,
            **referente
          } 
          # print( uo, resultado )
          alts = resultado['alturas'] 
          ints = resultado['intervalos'] 
          vozs = resultado['voces'] 
          durs = resultado['duraciones'] 
          dins = resultado['dinamicas'] 
          octa = resultado['octava']
          trar = resultado['transporte']

          pasos = len( max( alts, dins, durs ) )
          # Combinacion parametros: altura, duracion, dinamica, etc
          for paso in range( pasos ):
            alt  = alts[ paso % len( alts ) ]
            #Ajuste relacion puntero altura/int
            acor = []
            if alt != 0:
              alt = alt - 1
              nota = ints[ alt % len( ints ) ] + trar
              if vozs:
               # Voces, del set de inter
               for voz in vozs:
                 fund = alt + ( voz[ paso % len( voz ) ] - 1)
                 acor += [ ints[ fund % len( ints ) ]  + trar]
                 #acorde += [ voz[ paso % len( voz )  ] ]
            else:
              # Silencio
              nota = 'S'
            print(paso,alt,acor)  
            dur  = durs[ paso % len( durs ) ]
            din  = dins[ paso % len( dins ) ]


            evento = {
              'orden'      : paso,
              'altura'     : nota,
              'acorde'     : acor,
              'duracion'   : dur,
              'dinamica'   : din,
              'octava'     : octa,
              'transporte' : trar,
            }
            # print(evento)
            secuencia += [ evento ]
    return secuencia
    
"""
Clase para las unidades de cada track
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

cadena = stream.Stream()
for evento in t.secuencia:
    #print( evento )
    if evento['altura'] == 'S':
      nota = note.Rest()
    else:
      nota = note.Note()
      nota.pitch.ps = evento['altura'] 
      #nota.midi = evento['altura'] + evento['transporte']
      #nota.octave = evento['oct']
      if evento['acorde']:
        nota = chord.Chord( evento['acorde'] )
    duracion = duration.Duration( evento['duracion'] )
    nota.duration = duracion 
    dinamica = dynamics.Dynamic( evento['dinamica'] )
    nota.dynamic = dinamica
    cadena.append( nota )


acorde = chord.Chord([60,63,67,72])
cadena.append( acorde )
cadena.show()

"""
prope eval() https://docs.python.org/3/library/ast.html 

Cada unidad tiene o parametros propios o parametros 
que hereda o de los params generales o de otra unidad si es 
es "hija" lo cual lo indica el prefijo "^"
"""
"""
El secuencia de indices que define el largo del loop es el mas largo
"""
