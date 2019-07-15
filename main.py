from argumentos import args, verbose, Excepcion

import yaml
import pprint
from pista import Pista

def leer_yamls():
  """ Lee ficheros YAML declarados argumentos posicionales """
  defs = []
  for archivo in args.archivos:
    data = open( archivo.name, 'r' )
    try:
      y = yaml.load( data, Loader = yaml.FullLoader ) 
      #y = yaml.load( data ) 
      defs.append( y )
    except Exception as e:
      print( e )
      print( "=" * 80 )
  return defs

DEFS = leer_yamls()

""" A partir de cada definicion agrega una Pista """
#PISTAS = []
EVENTOS = []
for d in DEFS:
  pista = Pista(
    d[ 'nombre' ],
    d[ 'unidades' ],
    d[ 'forma' ],
  )
  # TODO ver si eshay q guardarlas 
  #PISTAS.append( pista )

  if args.verbose:
    print( pista.verbose( args.verbose ) )

  """ Generar canal MIDI a partir de cada pista """

  momento = 0
  track = pista.numero

  """ Parametros de Pista Primer articulación de la parte, agregar
  eventos fundamentales: pulso, armadura de clave, compás y programa.
  """

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

  for segmento in pista.segmentos:
    canal = segmento.canal
    momento += segmento.desplazar

    if momento < 0:
     raise ValueError( 'No se puede desplazar antes q el inicio' ) 
     pass

    """ Agregar propiedades de segmento.
    inserta etiquetas y modificadores de unidad (desplazar)."""

    if segmento.cambia( 'metro' ):
      EVENTOS.append([
        'addTimeSignature',
        track,
        momento,
        segmento.metro['numerador'],
        segmento.metro['denominador'],
        segmento.metro['relojes_por_tick'], 
        segmento.metro['notas_por_pulso']
      ])

    if segmento.cambia( 'bpm' ):
      EVENTOS.append([
        'addTempo',
        track,
        momento,
        segmento.bpm,
      ])

    if segmento.cambia( 'clave' ):
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

    for articulacion in segmento.articulaciones:

      """ Agrega cualquier cambio de parametro, 
      comparar cada uno con la articulacion previa. """

      if articulacion.cambia( 'bpm' ):
        EVENTOS.append([
          'addTempo',
          track,
          momento,
          articulacion.bpm,
        ])

      if articulacion.cambia( 'programa' ):
        EVENTOS.append([
           'addProgramChange',
           track,
           canal, 
           momento, 
           articulacion.programa
        ])

      if articulacion.letra:
        EVENTOS.append([
         'addText',
          track,
          momento,
          articulacion.letra
        ])

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

      if articulacion.controles:
        """ Agregar cambios de control """
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



