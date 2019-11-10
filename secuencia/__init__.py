from .pista import Pista
class Secuencia:

  """ Consolida Pistas.
  Recorre articulaciones y cambios de parámetros entre los elementos.
  Reúne todos los pronunciamientos en único flujo de instrucciones.
  """

  def __init__( 
      self,
      definiciones,
      verbose,
      copy
    ):
    self.definiciones = definiciones
    self.pistas = []
    self.verbose = verbose
    self.copyright = copy

    
    for d in self.definiciones:
      r = {
        **Pista.defactos,
        **d
      }
      pista = Pista(
        nombre    = r[ 'nombre' ],
        paleta    = r[ 'unidades' ],
        forma     = r[ 'forma' ],
        plugin    = r[ 'complementos' ],
        secuencia = self,
      )
      self.pistas.append( pista )

  @property
  def llamadas( self ):
    """ A partir de cada definicion agrega una Pista. """
    llamadas = []
    for pista in self.pistas:

      if self.verbose:
        print( pista.verbose( self.verbose ) )
    
      """ Generar track p/c pista """
      delta = 0
      track = pista.numero
    
      """ Parametros de Pista Primer articulación de la parte, agregar
      eventos fundamentales: pulso, armadura de clave, compás y programa.
      """
      llamadas.append([
        'addTrackName',
        track,
        delta,
        pista.nombre
      ])

      if self.copyright:
        llamadas.append([
          'addCopyright',
          track,
          delta,
          self.copyright
        ])
    
      """ Loop principal:
      Genera una secuencia de eventos MIDI lista de articulaciones.  """
    
      for segmento in pista.segmentos:
        canal = segmento.canal
        #delta += segmento.desplazar
    
        if delta < 0:
         raise ValueError( 'No se puede desplazar antes q el inicio' ) 
         pass
    
        """ Agregar propiedades de segmento. """
    
        if segmento.cambia( 'metro' ):
          llamadas.append([
            'addTimeSignature',
            track,
            delta,
            segmento.metro[ 'numerador' ],
            segmento.metro[ 'denominador' ],
            segmento.metro[ 'relojes_por_tick' ], 
            segmento.metro[ 'notas_por_pulso' ]
          ])
    
        if segmento.cambia( 'bpm' ):
          llamadas.append([
            'addTempo',
            track,
            delta,
            segmento.bpm,
          ])
    
        if segmento.cambia( 'clave' ):
          llamadas.append([
            'addKeySignature',
            track,
            delta,
            segmento.clave[ 'alteraciones' ],
            1, # multiplica por el n de alteraciones
            segmento.clave[ 'modo' ]
          ])
    
        if segmento.afinacionNota:
          llamadas.append([
           'changeNoteTuning',
            track, 
            segmento.afinacionNota[ 'afinaciones' ],
            segmento.afinacionNota[ 'canalSysEx' ],
            segmento.afinacionNota[ 'tiempoReal' ],
            segmento.afinacionNota[ 'programa' ],
          ])
    
        if segmento.afinacionBanco:
          llamadas.append([
            'changeTuningBank',
            track, 
            canal,
            delta,
            segmento.afinacionBanco[ 'banco' ],
            segmento.afinacionBanco[ 'ordenar' ],
          ])
    
        if segmento.afinacionPrograma:
          llamadas.append([ 
            'changeTuningProgram',
            track, 
            canal,
            delta,
            segmento.afinacionPrograma[ 'programa' ],
            segmento.afinacionPrograma[ 'ordenar' ],
          ])
    
        if segmento.sysEx:
          llamadas.append([
           'addSysEx',
            track, 
            delta, 
            segmento.sysEx[ 'fabricante' ],
            segmento.sysEx[ 'playload' ],
          ])
    
        if segmento.uniSysEx:
          llamadas.append([
           'addUniversalSysEx',
            track, 
            delta, 
            segmento.uniSysEx[ 'codigo' ],
            segmento.uniSysEx[ 'subCodigo' ],
            segmento.uniSysEx[ 'playload' ],
            segmento.uniSysEx[ 'canal' ],
            segmento.uniSysEx[ 'tiempoReal' ],
          ])
    
        if segmento.NRPN:
          llamadas.append([
           'makeNRPNCall',
            track, 
            canal, 
            delta, 
            segmento.NRPN[ 'control_msb' ],
            segmento.NRPN[ 'control_lsb' ],
            segmento.NRPN[ 'data_msb' ],
            segmento.NRPN[ 'data_lsb' ],
            segmento.NRPN[ 'ordenar' ],
          ])
    
        if segmento.RPN:
          llamadas.append([
           'makeRPNCall',
            track, 
            canal, 
            delta, 
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
            llamadas.append([
              'addTempo',
              track,
              delta,
              articulacion.bpm,
            ])
    
          if articulacion.cambia( 'programa' ):
            llamadas.append([
               'addProgramChange',
               track,
               canal, 
               delta, 
               articulacion.programa
            ])
    
          if articulacion.letra:
            llamadas.append([
             'addText',
              track,
              delta,
              articulacion.letra
            ])
    
          if articulacion.tono:
            llamadas.append([
               'addPitchWheelEvent',
               track,
               canal, 
               delta, 
               articulacion.tono
            ])
    
          """ Agregar nota/s (altura, duracion, dinamica).
          Si existe acorde en la articulación armar una lista con cada voz
          superpuesta.  o una lista de solamente un elemento.  """
          voces = [ articulacion.altura ]
          if articulacion.acorde:
            voces = articulacion.acorde 
    
          for voz in voces:
            if articulacion.dinamica:
              llamadas.append([
                'addNote',
                track, 
                canal, 
                voz, 
                delta, 
                articulacion.duracion, 
                articulacion.dinamica
              ])
            #else:
            #  print('eo')
    
          if articulacion.controles:
            """ Agregar cambios de control """
            for control in articulacion.controles:
              for control, valor in control.items():
                llamadas.append([
                 'addControllerEvent',
                  track, 
                  canal, 
                  delta, 
                  control,
                  valor, 
                ])
    
          delta += articulacion.duracion
    return llamadas
