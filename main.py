from argumentos import args, verboseprint
import yaml
from pista import Pista
from datetime import datetime, timedelta
import math

formato_tiempo =  '%H:%M:%S'

"""
Lee ficheros YAML declarados argumentos posicionales 
"""
DEFS = []
for archivo in args.archivos:
  data = open( archivo.name, 'r' )
  DEFS.append( yaml.load( data ) )

"""
A partir de cada definicion agrega una "Pista" 
"""
PISTAS = []
for d in DEFS:
  pista = Pista(
    d[ 'nombre' ],
    d[ 'unidades' ],
    d[ 'macroforma' ],
  )
  PISTAS.append( pista )

def referir(
  refs,
  o = None,
  ):
  """
  Extrae referentes recursivamente
  """
  referente   = refs[ 'referente' ]   if 'referente'   in refs else None
  nombre      = refs[ 'nombre' ]      if 'nombre'      in refs else None
  recurrencia = refs[ 'recurrencia' ] if 'recurrencia' in refs else None
  nivel       = refs[ 'nivel' ]       if 'nivel'       in refs else None
  output      = o                     if o is not None         else [ None ] * nivel 
  output[ nivel - 1 ] = ( nombre, recurrencia )
  if referente:
    referir( referente, output )
  return output

PARTES = []
"""
Inicializar tracks MIDI a partir de cada pista
"""
EVENTOS = []
for pista in PISTAS:
  momento = 0
  track = pista.orden
  EVENTOS.append([
    'addTrackName',
    track,
    momento,
    pista.nombre
  ])

  comienzo = datetime.strptime( 
    str( timedelta( seconds = 0 ) ),
    formato_tiempo 
  ) 
  parte = {
     'orden'     : track,
     'nombre'    : pista.nombre,
     'comienzo'  : comienzo, 
     'etiquetas' : [],
  }
  duracion_parte = 0

  """
  Loop principal:
  Convierte secuencia de articulaciones a eventos MIDI 
  TO DO: agregar funcciones de midiutil adicionales:
  https://midiutil.readthedocs.io/en/1.2.1/class.html#classref
  """
  for index, articulacion in enumerate( pista.secuencia ):
    verboseprint( articulacion )
    precedente   = pista.secuencia[ index - 1 ]
    unidad   = articulacion[ 'unidad' ]
    canal    = articulacion[ 'canal' ]
    bpm      = articulacion[ 'bpm' ]
    metro    = articulacion['metro'].split( '/' )
    clave    = articulacion[ 'clave' ]
    programa = articulacion[ 'programa' ]
    duracion = articulacion[ 'duracion' ] 

    """
    Primer articulación de la parte, agregar eventos fundamentales: Pulso,
    armadura de clave, compás y programa.
    """
    if ( index == 0 ):
      EVENTOS.append([
        'addTempo',
        track,
        momento,
        bpm
      ])

      """
      Clave de compás
      https://midiutil.readthedocs.io/en/1.2.1/class.html#midiutil.MidiFile.MIDIFile.addTimeSignature
      denominator  = potencia negativa de 2: log10( X ) / log10( 2 ) 
      2 representa  una negra, 3 una corchea, etc.
      """
      numerador        = int( metro[0] ) 
      denominador      = int( math.log10( int( metro[1] ) ) / math.log10( 2 ) )
      relojes_por_tick = 12 * denominador
      notas_por_pulso = 8
      EVENTOS.append([
        'addTimeSignature',
        track,
        momento,
        numerador,
        denominador,
        relojes_por_tick, 
        notas_por_pulso
      ])

      EVENTOS.append([
        'addKeySignature',
        track,
        momento,
        clave[ 'alteraciones' ],
        # multiplica por el n de alteraciones
        1, 
        clave[ 'modo' ]
      ])

      EVENTOS.append([
        'addProgramChange',
        track,
        canal,
        momento,  
        programa
      ])

    """
    Agrega cualquier cambio de parametro, 
    comparar cada uno con la articulacion previa.
    """
    if ( precedente['bpm'] != bpm ):
      EVENTOS.append([
        'addTempo',
        track,
        momento,
        bpm,
      ])

    if ( precedente[ 'metro' ] != metro ):
      numerador        = int( metro[ 0 ] ) 
      denominador      = int( math.log10( int( metro[ 1 ] ) ) / math.log10( 2 ) )
      relojes_por_tick = 12 * denominador
      notas_por_pulso = 8
      EVENTOS.append([
        'addTimeSignature',
        track,
        momento,
        numerador,
        denominador,
        relojes_por_tick, 
        notas_por_pulso
      ])

    if ( precedente[ 'clave' ] != clave ):
      EVENTOS.append([
        'addKeySignature',
        track,
        momento,
        clave[ 'alteraciones' ],
        1, # multiplica por el n de alteraciones
        clave[ 'modo' ]
      ])

    #if programa:
    if ( precedente[ 'programa' ] != programa ):
      EVENTOS.append([
         'addProgramChange',
         track,
         canal, 
         momento, 
         programa
      ])
    #midi_bits.addText( pista.orden, momento , 'prgm : #' + str( programa ) )

    """
    Primer articulacion de la Unidad,
    inserta etiquetas y modificadores de unidad (desplazar).
    """
    if ( articulacion[ 'orden' ] == 0 ):
      desplazar = articulacion[ 'desplazar' ]
      # TODO raise error si desplazar + duracion es negativo
      momento += desplazar 

      """
      Compone texto de la etiqueta a partir de nombre de unidad, numero de
      iteración y referentes
      """ 
      texto = ''
      ers = referir( articulacion[ 'referente' ] ) if articulacion[ 'referente' ] != None else [ ( 0, 0 ) ]
      prs = referir( precedente[ 'referente' ] ) if precedente[ 'referente' ] != None else [ ( 0, 0 ) ]
      for er, pr in zip( ers , prs ):
        if er != pr: 
          texto += str( er[ 0 ] ) + ' #' + str( er[ 1 ] ) + '\n' 
      texto += unidad 
      EVENTOS.append([
       'addText',
        track,
        momento,
        texto 
      ])
      
      etiqueta = {
        'texto'  : texto,
        'cuando' : momento,
        #'hasta' : duracion_unidad,
      }
      parte[ 'etiquetas' ].append( etiqueta ) 

    """
    Agregar nota/s (altura, duracion, dinamica).
    Si existe acorde en la articulación armar una lista con cada voces 
    o una lista de solamente un elemento.
    """
    voces = articulacion[ 'acorde' ] if articulacion[ 'acorde' ] else [ articulacion[ 'altura' ] ]
    dinamica = int( articulacion[ 'dinamica' ] * 126 )
    for voz in voces:
      altura = voz 
      """
      Si la articulacion es un silencio (S) agregar nota sin altura ni dinamica.
      """
      if voz == 'S':
        dinamica = 0
        altura = 0
      EVENTOS.append([
        'addNote',
        track, 
        canal, 
        altura, 
        momento, 
        duracion, 
        dinamica,
      ])

    """
    Agregar cambios de control
    """
    if articulacion[ 'controles' ]:
      for control in articulacion[ 'controles' ]:
        for c, v in control.items():
          EVENTOS.append([
           'addControllerEvent',
            track, 
            canal, 
            momento, 
            c,
            v, 
          ])
    momento += duracion
    duracion_parte += ( duracion *  60 ) / bpm 

  parte[ 'duracion' ] = datetime.strptime( 
    str( timedelta( seconds = duracion_parte  )   ).split( '.' )[0],
    formato_tiempo
  ) 
  PARTES.append( parte )
