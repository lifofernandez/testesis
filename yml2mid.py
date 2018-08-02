#!/usr/bin/env python3

import argparse
import yaml
import weakref
from music21 import *

"""
Manejo de argumentos y parametros globales
"""
parser = argparse.ArgumentParser()
parser.add_argument( 
 'archivos',
 help  = 'Al menos un archivo en formato YAML para procesar',
 type  = argparse.FileType('r'),
 nargs = '+'
)
parser.add_argument( 
 '-v',
 '--verbosity',
 help = 'Imprimir informacion',
)
parser.add_argument( 
 '-f',
 '--formato',
 help = 'Formato de salida (op: midi, musicxml, text).',
)
args = parser.parse_args()
# Archivos de entrada
pistas = []
for archivo in args.archivos:
  data = open( archivo.name, 'r' )
  pistas.append( yaml.load( data ) )
# Verbosidat
verboseprint = print if args.verbosity else lambda *a, **k: None
# Salida
formato_salida = args.formato 
# Sufijo herencia 
# (a^ = a + override con params propios)
sufijo_prima = '^' 

"""
Clase para cada track a partir de archivos.yml
"""
class Pista:
  cantidad = 0 
 
  def __init__( 
    self,
    constantes,
    default,
    originales,
    macroforma,
  ):
    self.constantes = constantes
    verboseprint( '\n#### ', self.constantes['nombre'], ' ####' )
    self.default    = default
    self.originales = originales 
    self.macroforma = macroforma
    self.secuencia  = self.secuenciar()
    Pista.cantidad += 1

  def __str__( self ):
    o = '' 
    for attr, value in self.__dict__.items():
      l = str( attr ) + ':' + str( value )
      o += l + '\n'
    return o

  # Paleta de Unidades
  @property
  def unidades( self ):
    unidades = {} 
    for unidad in self.originales:
      uo = Unidad( 
        unidad, 
        self.originales[ unidad ], 
        self.default,
        self
      )
      unidades[ unidad ] =  uo
    return unidades

  # Genera una secuencia a partir de los unidades/parametros
  # BUG: solo quedan hijas de la ultima unidad padre
  def secuenciar( 
    self,
    unidades = None,
    nivel = 0,
    pisar = {},
    s =  []
  ):
    unidades = unidades if unidades is not None else self.macroforma
    paleta = self.unidades
    nivel += 1
    sequencia = s
    secuencia = s if s is not None else secuencia
    for u in unidades:  
      verboseprint( '-' * ( nivel - 1 ) + str( u ) )
      if u in paleta:
        uo = paleta[ u ]
        # Mix propiedades con unidad referente
        referente = { **uo.propiedades, **pisar }
        if uo.unidades:
          sequencia = self.secuenciar( uo.unidades, nivel, referente, secuencia ) 
        # Solo unidades basicas (no UoUs) se secuencian 
        else: 
          # Mix parametros con unidad referente
          resu = { **uo.parametros, **referente } 
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
            acor = []
            if alt != 0:
              # Ajuste relacion puntero altura/int
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
            sequencia.append( evento )
    return sequencia

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

  @property 
  def es_hijo( self ):
    return self.nombre.endswith( sufijo_prima )

  @property  
  def apellido( self ):
    if self.es_hijo:
      # obtener nombre padre
      return self.nombre[0:-1]

  # Propiedades originales del padre
  @property  
  def herencia( self ):
    if self.apellido:
      # track() weakref del track que contiene esta unidad 
      herencia = self.track().originales[ self.apellido ]
      return herencia 

  # Mix de herencia con parametros originales
  @property # presindible?
  def sucesion( self ):
    if self.herencia:
      # mix dicts  
      o = { **self.herencia, **self.original }
      return o

  # Propiedades a partir originales (si no hay sucecion) ó sucesión con originales
  # TODO: revisar si propiedas y/o sucesion está de mas
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

  # Unidad de Unidades
  @property
  def unidades( self ):
    if 'unidades' in self.parametros:
      return self.parametros['unidades']
      
"""
Metodos generales

Devuelve el tamaño de la lista mas larga
https://stackoverflow.com/questions/30902558
"""
def larguest( l ):
    if( not isinstance( l, list ) ): return(0)
    return( 
      max( 
        [ len( l ) , ] + 
        [ len( subl ) for subl in l if isinstance( subl, list ) ] +
        [ larguest( subl ) for subl in l ]
      )
    )

"""
Loop principal:
Recorre cada pista y partir de su secuencia genera Notas o Silencios 
que agrupa en una Parte para finalmente agregarlas a una Partirtura de Musescore
"""
partitura = stream.Score()
for pista in pistas:
  p = Pista(
    pista['CONSTANTES'],
    pista['default'],
    pista['unidades'],
    pista['macroforma'],
  )
  parte = stream.Part()
  i = instrument.fromString( p.constantes['instrumento'] )
  parte.insert( i )

  for index, evento in enumerate( p.secuencia ):
    evento = p.secuencia[ index ]
    previo = p.secuencia[ index - 1 ]
    e = note.Note()
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
      tm = tempo.MetronomeMark( 
        None,
        bpm,
        note.Note( type='quarter' ) 
      )
      parte.append( tm )
    metro = evento['metro']
    if ( previo['metro'] != metro ):
      mt = meter.TimeSignature( metro )
      parte.append( mt )
    verboseprint( evento )
    parte.append( e )
  parte.makeMeasures()
  partitura.append( parte )

"""
Salida
"""
partitura.show( formato_salida )

