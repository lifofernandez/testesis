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

  """
  Loop principal:
  Genera una secuencia de eventos MIDI lista de articulaciones.
  """
  for segmento in ( pista.secuencia ):
    #print( segmento.articulaciones)
    for index, articulacion in enumerate( segmento.articulaciones ):

      """
      TO DO: agregar funcciones de midiutil adicionales:
      https://midiutil.readthedocs.io/en/1.2.1/class.html#classref
      [x] addCopyright
      [x] addPitchWheelEvent
      [x] changeNoteTunig
      [x] changeTuningBank
      [x] changeTuningProgram
      [x] addSysEx
      [x] addUniversalSysEx
      [x] makeNRPNCall
      [x] makeRPNCall
      """

      verboseprint( articulacion )
      precedente = segmento.articulaciones[ index - 1 ]
      unidad     = articulacion[ 'unidad' ]
      canal      = articulacion[ 'canal' ]
      bpm        = articulacion[ 'bpm' ]
      metro      = articulacion[ 'metro' ].split( '/' )
      clave      = articulacion[ 'clave' ]
      programa   = articulacion[ 'programa' ]
      duracion   = articulacion[ 'duracion' ] 
      tono       = articulacion[ 'tono' ] 

      """
      Primer articulación de la parte, agregar eventos fundamentales: pulso,
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
      TO DO: Crear estructura superiores a articulacion llamada segmento
      parametros de que ahora son relativios a la aritulacion #0
      """
      """
      Primer articulacion de la Unidad,
      inserta etiquetas y modificadores de unidad (desplazar).
      """
      if ( articulacion[ 'orden' ] == 0 ):
        desplazar = articulacion[ 'desplazar' ]

        # TODO raise error si desplazar + duracion es negativo
        momento += desplazar 
        #if ValueError( 

        """
        Compone texto de la etiqueta a partir de nombre de unidad, numero de
        iteración y referentes
        """ 
        texto = ''
        ers = [ ( 0, 0 ) ]
        if articulacion[ 'referente' ]:
          ers = referir( articulacion[ 'referente' ] ) 
        prs = [ ( 0, 0 ) ]
        if precedente[ 'referente' ]:
          prs = referir( precedente[ 'referente' ] )

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
        """
        changeNoteTuning
        """
        if articulacion[ 'afinacionNota' ]:
          EVENTOS.append([
           'changeNoteTuning',
            track, 
            articulacion[ 'afinacionNota' ][ 'afinaciones' ],
            articulacion[ 'afinacionNota' ][ 'canalSysEx' ],
            articulacion[ 'afinacionNota' ][ 'tiempoReal' ],
            articulacion[ 'afinacionNota' ][ 'programa' ],
          ])
        """
        changeTuningBank
        """
        if articulacion[ 'afinacionBanco' ]:
          EVENTOS.append([
            'changeTuningBank',
            track, 
            canal,
            momento,
            articulacion[ 'afinacionBanco' ][ 'banco' ],
            articulacion[ 'afinacionBanco' ][ 'ordenar' ],
          ])
        """
        changeTuningProgram
        """
        if articulacion[ 'afinacionPrograma' ]:
          EVENTOS.append([ 
            'changeTuningProgram',
            track, 
            canal,
            momento,
            articulacion[ 'afinacionPrograma' ][ 'programa' ],
            articulacion[ 'afinacionPrograma' ][ 'ordenar' ],
          ])
        """
        SysEx 
        """
        if articulacion[ 'sysEx' ]:
          EVENTOS.append([
           'addSysEx',
            track, 
            momento, 
            articulacion[ 'sysEx' ][ 'fabricante' ],
            articulacion[ 'sysEx' ][ 'playload' ],
          ])
        """
        UniversalSysEx 
        """
        if articulacion[ 'uniSysEx' ]:
          EVENTOS.append([
           'addUniversalSysEx',
            track, 
            momento, 
            articulacion[ 'uniSysEx' ][ 'codigo' ],
            articulacion[ 'uniSysEx' ][ 'subCodigo' ],
            articulacion[ 'uniSysEx' ][ 'playload' ],
            articulacion[ 'uniSysEx' ][ 'canal' ],
            articulacion[ 'uniSysEx' ][ 'tiempoReal' ],
          ])
        """
        Numero de Parametro No Registrado
        """
        if articulacion[ 'NRPN' ]:
          EVENTOS.append([
           'makeNRPNCall',
            track, 
            canal, 
            momento, 
            articulacion[ 'NRPN' ][ 'control_msb' ],
            articulacion[ 'NRPN' ][ 'control_lsb' ],
            articulacion[ 'NRPN' ][ 'data_msb' ],
            articulacion[ 'NRPN' ][ 'data_lsb' ],
            articulacion[ 'NRPN' ][ 'ordenar' ],
          ])

        """
        Numero de Parametro Registrado
        """
        if articulacion[ 'RPN' ]:
          EVENTOS.append([
           'makeRPNCall',
            track, 
            canal, 
            momento, 
            articulacion[ 'RPN' ][ 'control_msb' ],
            articulacion[ 'RPN' ][ 'control_lsb' ],
            articulacion[ 'RPN' ][ 'data_msb' ],
            articulacion[ 'RPN' ][ 'data_lsb' ],
            articulacion[ 'RPN' ][ 'ordenar' ],
          ])
        # Termina articulacion 0, estos van a ser parametros de Segmento

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

      if ( precedente[ 'tono' ] != tono ):
        EVENTOS.append([
           'addPitchWheelEvent',
           track,
           canal, 
           momento, 
           tono
        ])

      """
      Agregar nota/s (altura, duracion, dinamica).
      Si existe acorde en la articulación armar una lista con cada voz superpuesta. 
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
          for control, valor in control.items():
            EVENTOS.append([
             'addControllerEvent',
              track, 
              canal, 
              momento, 
              control,
              valor, 
            ])

      momento += duracion
      #duracion_parte += ( duracion *  60 ) / bpm 

