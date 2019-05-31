from argumentos import args, verboseprint, Excepcion
import yaml
from pista import Pista
from datetime import datetime, timedelta

formato_tiempo =  '%H:%M:%S'

""" Lee ficheros YAML declarados argumentos posicionales """
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

""" A partir de cada definicion agrega una Pista """
PISTAS = []
for d in DEFS:
  pista = Pista(
    d[ 'nombre' ],
    d[ 'unidades' ],
    d[ 'forma' ],
  )
  PISTAS.append( pista )

""" Generar canal MIDI a partir de cada pista """
EVENTOS = []
for pista in PISTAS:
  momento = 0
  track = pista.orden

  """ Parametros de Pista
  Primer articulación de la parte, agregar eventos fundamentales: pulso,
  armadura de clave, compás y programa.  """
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

  """ Loop principal: Genera una secuencia de eventos MIDI lista de
  articulaciones.  """
  for numero_segmento, segmento in enumerate( pista.secuencia ):
    print(segmento.pista, numero_segmento, segmento.orden)

    segmento_precedente = pista.secuencia[  numero_segmento - 1 ]
    if numero_segmento == 0:
      segmento_precedente = Pista.defacto
      
    canal = segmento.canal
    momento += segmento.desplazar

    if momento < 0:
     raise ValueError( 'No se puede desplazar antes q el inicio' ) 
     pass

    """ Compone texto de la etiqueta a partir de nombre de unidad, numero de
    iteración y referentes """ 
    texto = segmento.nombre
    #ers = [ ( 0, 0 ) ]
    #if segmento.referente:
    #  ers = segmento.referir( segmento.referente ) 
    #prs = [ ( 0, 0 ) ]
    #if segmento_precedente.referente:
    #  prs = segmento.referir( segmento_precedente.referente )
    #for er, pr in zip( ers , prs ):
    #  if er != pr: 
    #    texto += str( er[ 0 ] ) + ' #' + str( er[ 1 ] ) + '\n' 
    ##texto += segmento.nombre
    #if  segmento.referente:
    #  texto += segmento.nombre
    EVENTOS.append([
     'addText',
      track,
      momento,
      texto
    ])

    """ Agregar propiedades de segmento.
    inserta etiquetas y modificadores de unidad (desplazar)."""
    if segmento_precedente.metro != segmento.metro:
      EVENTOS.append([
        'addTimeSignature',
        track,
        momento,
        segmento.metro['numerador'],
        segmento.metro['denominador'],
        segmento.metro['relojes_por_tick'], 
        segmento.metro['notas_por_pulso']
      ])
    if segmento_precedente.bpm != segmento.bpm:
      EVENTOS.append([
        'addTempo',
        track,
        momento,
        segmento.bpm,
      ])
    if segmento_precedente.clave != segmento.clave:
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

    for numero_articulacion, articulacion in enumerate( segmento.articulaciones ):
      articulacion_precedente = segmento.articulaciones[  numero_articulacion - 1 ]
      if  numero_articulacion == 0:
        articulacion_precedente = segmento_precedente.articulaciones[ - 1 ]
      verboseprint( articulacion )
      """ Agrega cualquier cambio de parametro, 
      comparar cada uno con la articulacion previa. """
      if articulacion_precedente.bpm != articulacion.bpm:
        EVENTOS.append([
          'addTempo',
          track,
          momento,
          articulacion.bpm,
        ])

      if articulacion_precedente.programa != articulacion.programa:
        EVENTOS.append([
           'addProgramChange',
           track,
           canal, 
           momento, 
           articulacion.programa
        ])
        #midi_bits.addText( pista.orden, momento , 'prgm : #' + str( programa ) )

      if articulacion.tono:
        EVENTOS.append([
           'addPitchWheelEvent',
           track,
           canal, 
           momento, 
           articulacion.tono
        ])

      """ Agregar nota/s (altura, duracion, dinamica).
      Si existe acorde en la articulación armar una lista con cada voz
      superpuesta.  o una lista de solamente un elemento.  """
      voces = [ articulacion.altura ]
      if articulacion.acorde:
        voces = articulacion.acorde 

      dinamica = articulacion.dinamica
      for voz in voces:
        altura = voz 
        """ Si la articulacion es un silencio (S) agregar nota sin altura ni 
        dinamica.  """
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
          dinamica,
        ])
      """ Agregar cambios de control """
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

