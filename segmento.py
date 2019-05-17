from argumentos import args, verboseprint, Excepcion
from articulacion import Articulacion

import random

class Segmento:
  """
  Pista > Secuencia > SEGMENTOS > Articulaciones
  """
  cantidad = 0 
 
  def __str__( self ):
    o = '' 
    for attr, value in self.__dict__.items():
      l = str( attr ) + ':' + str( value )
      o += l + '\n'
    return o

  def __init__( 
    self,
    unidad,
  ):
    self.orden = Segmento.cantidad 
    Segmento.cantidad += 1

    self.nombre            = unidad[ 'nombre' ]
    self.canal             = unidad[ 'canal' ]
    self.reiterar          = unidad[ 'reiterar' ]
    self.revertir          = unidad[ 'revertir' ]
    self.desplazar         = unidad[ 'desplazar' ]
    self.transponer        = unidad[ 'transponer' ]
    self.transportar       = unidad[ 'transportar' ]
    self.referente         = unidad[ 'referente' ]
    self.clave             = unidad[ 'clave' ]
    self.metro             = unidad[ 'metro' ]
    self.afinacionNota     = unidad[ 'afinacionNota' ]
    self.afinacionBanco    = unidad[ 'afinacionBanco' ]
    self.afinacionPrograma = unidad[ 'afinacionPrograma' ]
    self.sysEx             = unidad[ 'sysEx' ]
    self.uniSysEx          = unidad[ 'uniSysEx' ]
    self.NRPN              = unidad[ 'NRPN' ]
    self.RPN               = unidad[ 'RPN' ]
    self.registracion      = unidad[ 'registracion' ]

    self.programas         = unidad[ 'programas' ]
    self.duraciones        = unidad[ 'duraciones' ]
    self.BPMs              = unidad[ 'BPMs' ]
    self.dinamicas         = unidad[ 'dinamicas' ]
    self.fluctuacion       = unidad[ 'fluctuacion' ]
    self.alturas           = unidad[ 'alturas' ]
    self.tonos             = unidad[ 'tonos' ]
    self.voces             = unidad[ 'voces' ]
    self.capas             = unidad[ 'controles' ]

    """ PRE PROCESO DE UNIDAD
    Cambia el sentido de los parametros del tipo lista """

    #TODO: ¿convertir cualquier string o int en lista?

    #for attr, value in self.__dict__.items():
    #    print( attr )
    #if 'revertir' in unidad:
    #  revertir = unidad[ 'revertir' ] 
    #  if isinstance( revertir , list ): 
    #    for r in revertir:
    #      if r in unidad:
    #        unidad[ r ].reverse() 
    #  elif isinstance( revertir , str ):
    #    if revertir in unidad:
    #      unidad[ revertir ].reverse() 

    self.ganador_voces = [ 0 ]
    if self.voces:
      self.ganador_voces = max( self.voces, key = len) 
    self.ganador_capas = [ 0 ]
    if self.capas:
      self.ganador_capas = max( self.capas , key = len) 

    """ Evaluar que parametro lista es el que mas valores tiene.  """
    candidatos = [ 
      self.dinamicas,
      self.duraciones,
      self.alturas,
      self.tonos,
      self.BPMs,
      self.programas,
      self.ganador_voces,
      self.ganador_capas,
    ]
    ganador = max( candidatos, key = len )
    self.pasos = len( ganador )

    # TO DO
    rand_min = 0
    if 'min' in self.fluctuacion:
        rand_min = self.fluctuacion['min'] 
    rand_max = 0
    if 'max' in self.fluctuacion:
        rand_max = self.fluctuacion['max']
    self.fluctuacion = random.uniform( 
        rand_min,
        rand_max 
    ) if rand_min or rand_max else 1

    """ Consolidad "articulacion" 
    combinar parametros: altura, duracion, dinamica, etc. """
    self.articulaciones = []
    for paso in range( self.pasos ):
      """ Alturas, voz y superposición voces. """
      altura = self.alturas[ paso % len( self.alturas ) ]
      acorde = []
      nota   = 'S' # Silencio
      if altura != 0:
        """ Relacion: altura > puntero en el set de registracion; Trasponer
        dentro del set de registracion, luego Transportar, sumar a la nota
        resultante. """
        n = self.registracion[ ( ( altura - 1 ) + self.transponer ) % len( self.registracion ) ] 
        nota = self.transportar + n
        """ Armar superposicion de voces. """
        if self.voces:
          for v in self.voces:
            voz = ( altura + ( v[ paso % len( v ) ] ) - 1 ) + self.transponer
            acorde += [ self.transportar +  self.registracion[ voz % len( self.registracion ) ]  ]
      """ Cambios de control. """
      controles = []
      if self.capas:
        for capa in self.capas:
          controles += [ capa[ paso % len( capa ) ] ]
      """ Articulación a secuenciar. """
      articulacion = Articulacion(
         nombre    = str( self.orden ) + self.nombre + str( paso ),
         paso      = paso,
         bpm       = self.BPMs[ paso % len( self.BPMs ) ],
         programa  = self.programas[ paso % len( self.programas ) ],
         duracion  = self.duraciones[ paso % len( self.duraciones ) ],
         dinamica  = self.dinamicas[ paso % len( self.dinamicas ) ] * self.fluctuacion,
         tono      = self.tonos[ paso % len( self.tonos ) ],
         nota      = nota,
         acorde    = acorde,
         controles = controles,
      )
      self.articulaciones.append( articulacion )
    #self.articulaciones = self._articulaciones

