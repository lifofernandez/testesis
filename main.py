from argumentos import args, verboseprint, Excepcion
import yaml
from pista import Pista
from datetime import datetime, timedelta
import math

formato_tiempo =  '%H:%M:%S'

"""
Lee ficheros YAML declarados argumentos posicionales 
"""
def leer_yamls():
  defs = []
  for archivo in args.archivos:
    data = open( archivo.name, 'r' )
    try:
      y = yaml.load( data ) 
      defs.append( y )
    except Exception as e:
      print(e)
      print( "=" * 80)
  return defs
DEFS = leer_yamls()

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

"""
Extrae referentes recursivamente
"""
def referir(
    refs,
    o = None,
  ):
  referente   = refs[ 'referente' ]   if 'referente'   in refs else None
  nombre      = refs[ 'nombre' ]      if 'nombre'      in refs else None
  recurrencia = refs[ 'recurrencia' ] if 'recurrencia' in refs else None
  nivel       = refs[ 'nivel' ]       if 'nivel'       in refs else None
  output      = o                     if o is not None         else [ None ] * nivel 
  output[ nivel - 1 ] = ( nombre, recurrencia )
  if referente:
    referir( referente, output )
  return output


"""
Generar canal MIDI a partir de cada pista
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

  EVENTOS.append([
    'addCopyright',
    track,
    momento,
    args.copyright
  ])

  #duracion_parte = 0
  segmentoP =  pista.secuencia[0] 
  articulacionP = segmentoP.articulaciones[0]

  """
  parametros de Parte /pista
  Primer articulación de la parte, agregar eventos fundamentales: pulso,
  armadura de clave, compás y programa.
  """
  EVENTOS.append([
    'addTempo',
    track,
    momento,
    articulacionP.bpm,
  ])

  """
  Clave de compás
  https://midiutil.readthedocs.io/en/1.2.1/class.html#midiutil.MidiFile.MIDIFile.addTimeSignature
  denominator  = potencia negativa de 2: log10( X ) / log10( 2 ) 
  2 representa  una negra, 3 una corchea, etc.
  primer_metro = articulacion2['metro'],
  """
  ##primer_metro = articulacionP[ 'metro' ].split( '/' )
  #numerador        = int( primer_metro[0] ) 
  #denominador      = int( math.log10( int( primer_metro[1] ) ) / math.log10( 2 ) )
  #relojes_por_tick = 12 * denominador
  #notas_por_pulso = 8
  #EVENTOS.append([
  #  'addTimeSignature',
  #  track,
  #  momento,
  #  numerador,
  #  denominador,
  #  relojes_por_tick, 
  #  notas_por_pulso
  #])

  #primer_clave = articulacionP['clave']
  #EVENTOS.append([
  #  'addKeySignature',
  #  track,
  #  momento,
  #  primer_clave[ 'alteraciones' ],
  #  # multiplica por el n de alteraciones
  #  1, 
  #  primer_clave[ 'modo' ]
  #])

  EVENTOS.append([
    'addProgramChange',
    track,
    #articulacionP['canal'],
    segmentoP.canal,
    momento,  
    articulacionP.programa
  ])

  """
  Loop principal:
  Genera una secuencia de eventos MIDI lista de articulaciones.
  """
  for numero_segmento, segmento in enumerate( pista.secuencia ):
    segmento_precedente = pista.secuencia[  numero_segmento - 1 ]
    canal = segmento.canal


    momento += segmento.desplazar
    if momento < 0 :
     raise ValueError( 'No se puede desplazar antes q el inicio' ) 
     pass

    #"""
    #Compone texto de la etiqueta a partir de nombre de unidad, numero de
    #iteración y referentes
    #""" 
    #texto = ''
    #ers = [ ( 0, 0 ) ]
    #if articulacion[ 'referente' ]:
    #  ers = referir( articulacion[ 'referente' ] ) 
    #prs = [ ( 0, 0 ) ]
    #if precedente[ 'referente' ]:
    #  prs = referir( precedente[ 'referente' ] )

    #for er, pr in zip( ers , prs ):
    #  if er != pr: 
    #    texto += str( er[ 0 ] ) + ' #' + str( er[ 1 ] ) + '\n' 
    #texto += unidad 
    #if  segmento.referente:

    """
    Agregar propiedades de segmento
    inserta etiquetas y modificadores de unidad (desplazar).
    """
    EVENTOS.append([
     'addText',
      track,
      momento,
      segmento.nombre
    ])

    metro = segmento.metro.split( '/' ) 
    if ( segmento_precedente.metro.split( '/' ) != metro):
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

    if ( segmento_precedente.clave != segmento.clave ):
      EVENTOS.append([
        'addKeySignature',
        track,
        momento,
        segmento.clave[ 'alteraciones' ],
        1, # multiplica por el n de alteraciones
        segmento.clave[ 'modo' ]
      ])


    if segmento.afinacionNota:
      EVENTOS.append([
       'changeNoteTuning',
        track, 
        segmento.afinacionNota[ 'afinaciones' ],
        segmento.afinacionNota[ 'canalSysEx' ],
        segmento.afinacionNota[ 'tiempoReal' ],
        segmento.afinacionNota[ 'programa' ],
      ])
    if segmento.afinacionBanco:
      EVENTOS.append([
        'changeTuningBank',
        track, 
        canal,
        momento,
        segmento.afinacionBanco[ 'banco' ],
        segmento.afinacionBanco[ 'ordenar' ],
      ])
    if segmento.afinacionPrograma:
      EVENTOS.append([ 
        'changeTuningProgram',
        track, 
        canal,
        momento,
        segmento.afinacionPrograma[ 'programa' ],
        segmento.afinacionPrograma[ 'ordenar' ],
      ])
    if segmento.sysEx:
      EVENTOS.append([
       'addSysEx',
        track, 
        momento, 
        segmento.sysEx[ 'fabricante' ],
        segmento.sysEx[ 'playload' ],
      ])
    if segmento.uniSysEx:
      EVENTOS.append([
       'addUniversalSysEx',
        track, 
        momento, 
        segmento.uniSysEx[ 'codigo' ],
        segmento.uniSysEx[ 'subCodigo' ],
        segmento.uniSysEx[ 'playload' ],
        segmento.uniSysEx[ 'canal' ],
        segmento.uniSysEx[ 'tiempoReal' ],
      ])
    if segmento.NRPN:
      EVENTOS.append([
       'makeNRPNCall',
        track, 
        canal, 
        momento, 
        segmento.NRPN[ 'control_msb' ],
        segmento.NRPN[ 'control_lsb' ],
        segmento.NRPN[ 'data_msb' ],
        segmento.NRPN[ 'data_lsb' ],
        segmento.NRPN[ 'ordenar' ],
      ])
    if segmento.RPN:
      EVENTOS.append([
       'makeRPNCall',
        track, 
        canal, 
        momento, 
        segmento.RPN[ 'control_msb' ],
        segmento.RPN[ 'control_lsb' ],
        segmento.RPN[ 'data_msb' ],
        segmento.RPN[ 'data_lsb' ],
        segmento.RPN[ 'ordenar' ],
      ])

    #REVISAR

    unidad = segmento.nombre
    metro  = segmento.metro.split( '/' )
    clave  = segmento.clave
    for numero_articulacion, articulacion in enumerate( segmento.articulaciones ):
      articulacion_precedente = segmento.articulaciones[  numero_articulacion - 1 ]

      if  numero_articulacion == 0:
        articulacion_precedente = segmento_precedente.articulaciones[ - 1 ]

      verboseprint( articulacion )

      """
      Agrega cualquier cambio de parametro, 
      comparar cada uno con la articulacion previa.
      """
      if ( articulacion_precedente.bpm != articulacion.bpm ):
        #print( articulacion_precedente.bpm, articulacion.bpm )
        EVENTOS.append([
          'addTempo',
          track,
          momento,
          articulacion.bpm,
        ])

      if ( articulacion_precedente.programa != articulacion.programa ):
        EVENTOS.append([
           'addProgramChange',
           track,
           canal, 
           momento, 
           articulacion.programa
        ])
        #midi_bits.addText( pista.orden, momento , 'prgm : #' + str( programa ) )

      if ( articulacion_precedente.tono != articulacion.tono ):
        EVENTOS.append([
           'addPitchWheelEvent',
           track,
           canal, 
           momento, 
           articulacion.tono
        ])

      """
      Agregar nota/s (altura, duracion, dinamica).
      Si existe acorde en la articulación armar una lista con cada voz superpuesta. 
      o una lista de solamente un elemento.
      """
      voces = [ articulacion.altura ]
      if articulacion.acorde:
        voces = articulacion.acorde 

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
          articulacion.duracion, 
          int( articulacion.dinamica * 126 ),
        ])


      """
      Agregar cambios de control
      """
      if articulacion.controles:
        for control in articulacion.controles:
          for control, valor in control.items():
            EVENTOS.append([
             'addControllerEvent',
              track, 
              canal, 
              momento, 
              control,
              valor, 
            ])

      momento += articulacion.duracion
      #duracion_parte += ( duracion *  60 ) / bpm 

