#!/usr/bin/env python3

import argparse
import yaml
import weakref
from music21 import *

parser = argparse.ArgumentParser()
parser.add_argument( 
 'archivos',
 help  = 'archivos yml para procesar',
 type  = argparse.FileType('r'),
 nargs = '+'
)
parser.add_argument( 
 '-v',
 '--verbosity',
 help='eo eio eo',
)
args = parser.parse_args()

# BUG: no respeta parametros (alturas, voces) de diferentes pistas
pistas = []
for archivo in args.archivos:
  data = open( archivo.name, 'r' )
  pistas.append( yaml.load( data ) )

if args.verbosity:
  print(args.verbosity)

# sufijo herencia (a^ = a + override con params propios)
sufijo_prima = '^' 

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
    self.secuencia  = self.secuenciar()
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
      print( '-' * ( nivel - 1 ) + str( u ) )
      if u in paleta:
        uo = paleta[ u ]
        # Mix propiedades con unidad referente
        referente = { **uo.propiedades, **pisar }
        if uo.unidades:
          us = uo.unidades
          self.secuenciar( us, nivel, secuencia, referente) 
        else: 
          # Solo unidades basicas (no UoUs) se secuencian 
          resu = { **uo.parametros, **referente } 
          #print( uo, resu )
          bpm  = resu['bpm']        if 'bpm'        in resu else 60 
          metr = resu['metro']      if 'metro'      in resu else '4/4'
          alts = resu['alturas']    if 'alturas'    in resu else [1] 
          ints = resu['intervalos'] if 'intervalos' in resu else [1]
          vozs = resu['voces']      if 'voces'      in resu else None
          durs = resu['duraciones'] if 'duraciones' in resu else [1]
          dins = resu['dinamicas']  if 'dinamicas'  in resu else [1]
          octa = resu['octava']     if 'octava'     in resu else None
          trar = resu['transporte'] if 'transporte' in resu else 0
          candidatos = [ dins, durs, alts ]
          pasos = larguest( candidatos )
          # Combinar parametros: altura, duracion, dinamica, etc
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
            else:
              # Silencio
              nota = 'S'
            # print(paso,alt,acor)  
            dur  = durs[ paso % len( durs ) ]
            din  = dins[ paso % len( dins ) ]
            evento = {
              'orden'      : paso,
              'bpm'        : bpm,
              'metro'      : metr,
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

  @property # presindible?
  def apellido( self ):
    if self.es_hijo:
      # obtener nombre padre
      return self.nombre[0:-1]

  @property # presindible?
  def herencia( self ):
    if self.apellido:
      # track() weakref track 
      herencia = self.track().originales[ self.apellido ]
      return herencia 

  @property # presindible?º
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
      

# https://stackoverflow.com/questions/30902558
def larguest( l ):
    if( not isinstance( l, list ) ): return(0)
    return( 
      max( 
        [ len( l ) , ] + 
        [ len( subl ) for subl in l if isinstance( subl, list ) ] +
        [ larguest( subl ) for subl in l ]
      )
    )


cadena = stream.Stream()
for pista in pistas:
  t = Track(
    pista['default'],
    pista['unidades'],
    pista['macroforma'],
  )
  parte = stream.Part()
  for index, evento in enumerate( t.secuencia ):
    evento = t.secuencia[ index ]
    previo = t.secuencia[ index - 1 ]
    if evento['altura'] == 'S':
      e = note.Rest()
    else:
      e = note.Note()
      e.pitch.ps = evento['altura'] 
      #nota.pitch.midi = evento['altura'] 
      #nota.octave = evento['oct']
      if evento['acorde']:
        e = chord.Chord( evento['acorde'] )
    duracion = duration.Duration( evento['duracion'] )
    e.duration = duracion 
    dinamica = dynamics.Dynamic( evento['dinamica'] )
    e.dynamic = dinamica
    bpm = evento['bpm']
    if ( previo['bpm'] != bpm ):
      tm = tempo.MetronomeMark( None, bpm, note.Note( type='quarter' ) )
      parte.append( tm )
    metro = evento['metro']
    if ( previo['metro'] != metro ):
      mt = meter.TimeSignature( metro )
      parte.append( mt )
    parte.append( e )
  parte.makeMeasures()
  cadena.append( parte )

# TODO: Poder elegir output (MIDI, MuseScore, etc)
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
