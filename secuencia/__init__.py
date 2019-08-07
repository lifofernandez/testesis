import os
from argumentos import args, verbose, Excepcion
from .pista import Pista
from .complementos import Complemento

class Secuencia:

  def __init__( 
      self,
      defs
    ):
    self.defs = defs 
    self.pistas = []
    #self.complementos = []
    
    for d in defs:
      pista = Pista(
        nombre = d[ 'nombre' ],
        paleta = d[ 'unidades' ],
        forma = d[ 'forma' ],
        secuencia = self,
      )
      self.pistas.append( pista )

  @property
  def complementos(
      self,
    ):
    complementos = []
    for d in self.defs:
      if 'complementos' in d:
       p = d[ 'complementos' ] 
       if os.path.exists( p ):
         #and p not in Complemento.registro:
         Complemento.registro.append( p )
         c = Complemento( p )
         complementos.append( c )
    return complementos

  @property
  def eventos( 
      self
    ):
    """ A partir de cada definicion agrega una Pista. """
    EVENTOS = []
    for pista in self.pistas:

      if args.verbose:
        print( pista.verbose( args.verbose ) )
    
      """ Generar track p/c pista """
    
      delta = 0
      track = pista.numero
    
      """ Parametros de Pista Primer articulación de la parte, agregar
      eventos fundamentales: pulso, armadura de clave, compás y programa.
      """
      EVENTOS.append([
        'addTrackName',
        track,
        delta,
        pista.nombre
      ])
      EVENTOS.append([
        'addCopyright',
        track,
        delta,
        args.copyright
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
          EVENTOS.append([
            'addTimeSignature',
            track,
            delta,
            segmento.metro[ 'numerador' ],
            segmento.metro[ 'denominador' ],
            segmento.metro[ 'relojes_por_tick' ], 
            segmento.metro[ 'notas_por_pulso' ]
          ])
    
        if segmento.cambia( 'bpm' ):
          EVENTOS.append([
            'addTempo',
            track,
            delta,
            segmento.bpm,
          ])
    
        if segmento.cambia( 'clave' ):
          EVENTOS.append([
            'addKeySignature',
            track,
            delta,
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
            delta,
            segmento.afinacionBanco[ 'banco' ],
            segmento.afinacionBanco[ 'ordenar' ],
          ])
    
        if segmento.afinacionPrograma:
          EVENTOS.append([ 
            'changeTuningProgram',
            track, 
            canal,
            delta,
            segmento.afinacionPrograma[ 'programa' ],
            segmento.afinacionPrograma[ 'ordenar' ],
          ])
    
        if segmento.sysEx:
          EVENTOS.append([
           'addSysEx',
            track, 
            delta, 
            segmento.sysEx[ 'fabricante' ],
            segmento.sysEx[ 'playload' ],
          ])
    
        if segmento.uniSysEx:
          EVENTOS.append([
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
          EVENTOS.append([
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
          EVENTOS.append([
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
            EVENTOS.append([
              'addTempo',
              track,
              delta,
              articulacion.bpm,
            ])
    
          if articulacion.cambia( 'programa' ):
            EVENTOS.append([
               'addProgramChange',
               track,
               canal, 
               delta, 
               articulacion.programa
            ])
    
          if articulacion.letra:
            EVENTOS.append([
             'addText',
              track,
              delta,
              articulacion.letra
            ])
    
          if articulacion.tono:
            EVENTOS.append([
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
            EVENTOS.append([
              'addNote',
              track, 
              canal, 
              voz, 
              delta, 
              articulacion.duracion, 
              articulacion.dinamica
            ])
    
          if articulacion.controles:
            """ Agregar cambios de control """
            for control in articulacion.controles:
              for control, valor in control.items():
                EVENTOS.append([
                 'addControllerEvent',
                  track, 
                  canal, 
                  delta, 
                  control,
                  valor, 
                ])
    
          delta += articulacion.duracion
    return EVENTOS
