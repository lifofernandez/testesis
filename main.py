from argumentos import args, verboseprint
import yaml
from pista import Pista
from datetime import datetime, timedelta
import math
formato_tiempo =  '%H:%M:%S'

DEFS = []
for archivo in args.archivos:
  """
  Lee ficheros YAML como argumentos posicionales 
  """
  data = open( archivo.name, 'r' )
  DEFS.append( yaml.load( data ) )

PISTAS = []
for d in DEFS:
  """
  Carga de pistas a partir de las definiciones
  """
  pista = Pista(
    d[ 'nombre' ],
    #d[ 'base' ],
    d[ 'unidades' ],
    d[ 'macroforma' ],
  )
  PISTAS.append( pista )

def referir(
  refs,
  o = None,
  ):
  """
  Comprueba referentes recursivamente
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

EVENTOS_MIDI = []
PARTES = []
for pista in PISTAS:
  """
  Loop principal:
  Convierte secuencia de eventos a eventos midi
  TODO: agregar funcciones de midiutil adicionales:
  https://midiutil.readthedocs.io/en/1.2.1/class.html#classref
  """
  momento = 0
  track = pista.orden

  EVENTOS_MIDI.append([
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

  for index, evento in enumerate( pista.secuencia ):
    verboseprint( evento )
    previo = pista.secuencia[ index - 1 ]
    unidad = evento[ 'unidad' ]
    previa = previo[ 'unidad' ]

    canal = evento[ 'canal' ]
    bpm   = evento[ 'bpm' ]
    metro = evento['metro'].split( '/' )
    #metro = evento[ 'metro' ]
    clave = evento[ 'clave' ]
    programa = evento[ 'programa' ]
    duracion_evento = evento[ 'duracion' ] 

    if ( index == 0 ):
      EVENTOS_MIDI.append([
        'addTempo',
        track,
        momento,
        bpm
      ])

      """
      Time Signature event
      https://midiutil.readthedocs.io/en/1.2.1/class.html#midiutil.MidiFile.MIDIFile.addTimeSignature
      denominator  = negative power of two: log10( X ) / log10( 2 ) 
      2 represents a quarter-note, 3 an eighth-note, etc.
      """
      numerador        = int( metro[0] ) 
      denominador      = int( math.log10( int( metro[1] ) ) / math.log10( 2 ) )
      relojes_por_tick = 12 * denominador
      notas_por_pulso = 8
      EVENTOS_MIDI.append([
        'addTimeSignature',
        track,
        momento,
        numerador,
        denominador,
        relojes_por_tick, 
        notas_por_pulso
      ])

      EVENTOS_MIDI.append([
        'addKeySignature',
        track,
        momento,
        clave[ 'alteraciones' ],
        1, # multiplica por el n de alteraciones
        clave[ 'modo' ]
      ])

      EVENTOS_MIDI.append([
        'addProgramChange',
        track,
        canal,
        momento,  
        programa
      ])

    if ( previo['bpm'] != bpm ):
      EVENTOS_MIDI.append([
        'addTempo',
        track,
        momento,
        bpm,
      ])

    if ( previo[ 'metro' ] != metro ):
      numerador        = int( metro[ 0 ] ) 
      denominador      = int( math.log10( int( metro[ 1 ] ) ) / math.log10( 2 ) )
      relojes_por_tick = 12 * denominador
      notas_por_pulso = 8
      EVENTOS_MIDI.append([
        'addTimeSignature',
        track,
        momento,
        numerador,
        denominador,
        relojes_por_tick, 
        notas_por_pulso
      ])

    if ( previo[ 'clave' ] != clave ):
      EVENTOS_MIDI.append([
        'addKeySignature',
        track,
        momento,
        clave[ 'alteraciones' ],
        1, # multiplica por el n de alteraciones
        clave[ 'modo' ]
      ])

    if programa:
      if ( previo[ 'programa' ] != programa ):
        EVENTOS_MIDI.append([
          'addProgramChange',
          track,
          canal, 
          momento, 
          programa
        ])
        #midi_bits.addText( pista.orden, momento , 'prgm : #' + str( programa ) )


    if ( evento[ 'orden' ] == 0 ):
      # al igual que revertir, es un modificador de unidad...
      desplazar = evento[ 'desplazar' ] 
      momento += desplazar 

      texto = ''
      ers = referir( evento[ 'referente' ] ) if evento[ 'referente' ] != None else [ ( 0, 0 ) ]
      prs = referir( previo[ 'referente' ] ) if previo[ 'referente' ] != None else [ ( 0, 0 ) ]
      for er, pr in zip( ers , prs ):
        if er != pr: 
          texto += str( er[ 0 ] ) + ' #' + str( er[ 1 ] ) + '\n' 
      texto += unidad 

      EVENTOS_MIDI.append([
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

    voces = evento[ 'acorde' ] if evento[ 'acorde' ] else [ evento[ 'altura' ] ]
    dinamica = int( evento[ 'dinamica' ] * 126 )
    for voz in voces:
      altura = voz 
      if voz == 'S':
        dinamica = 0
        altura = 0
      EVENTOS_MIDI.append([
        'addNote',
        track, 
        canal, 
        altura, 
        momento, 
        duracion_evento, 
        dinamica,
      ])

    if evento[ 'controlador' ]:
      for controlador, parametro in evento[ 'controlador' ].items():
        EVENTOS_MIDI.append([
         'addControllerEvent',
          track, 
          canal, 
          momento, 
          controlador, 
          parametro, 
        ])
    momento += duracion_evento
    duracion_parte += duracion_evento * ( 60 / bpm )

  parte[ 'duracion' ] = datetime.strptime( 
    str( timedelta( seconds = duracion_parte ) ).split( '.' )[0],
    formato_tiempo
  ) 
  PARTES.append( parte )
