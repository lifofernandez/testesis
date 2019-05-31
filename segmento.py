from argumentos import args, verboseprint, Excepcion
from articulacion import Articulacion
import random
import math
import pprint

class Segmento:
  """
  Pista > SEGMENTOS > Articulaciones
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
    pista, 
    orden,
    unidad,
  ):
    self.pista = pista 
    self.numero = Segmento.cantidad 
    Segmento.cantidad += 1

    self.original = unidad
    self.nombre = self.original[ 'nombre' ]

    """ PRE PROCESO DE UNIDAD """
    """ Cambia el sentido de los parametros de articulacion """
    self.revertir = self.original[ 'revertir' ]
    if self.revertir:
      if isinstance( self.revertir , list ): 
        for r in self.revertir:
          if r in self.original:
            self.original[ r ].reverse() 
      elif isinstance( self.revertir , str ):
        if revertir in self.original:
          self.original[ self.revertir ].reverse() 

    self.canal             = self.original[ 'canal' ]
    self.reiterar          = self.original[ 'reiterar' ]
    self.desplazar         = self.original[ 'desplazar' ]
    self.transponer        = self.original[ 'transponer' ]
    self.transportar       = self.original[ 'transportar' ]
    self.referente         = self.original[ 'referente' ]
    self.clave             = self.original[ 'clave' ]

    self.afinacionNota     = self.original[ 'afinacionNota' ]
    self.afinacionBanco    = self.original[ 'afinacionBanco' ]
    self.afinacionPrograma = self.original[ 'afinacionPrograma' ]
    self.sysEx             = self.original[ 'sysEx' ]
    self.uniSysEx          = self.original[ 'uniSysEx' ]
    self.NRPN              = self.original[ 'NRPN' ]
    self.RPN               = self.original[ 'RPN' ]
    self.registracion      = self.original[ 'registracion' ]

    self.programas         = self.original[ 'programas' ]
    self.duraciones        = self.original[ 'duraciones' ]
    self.BPMs              = self.original[ 'BPMs' ]
    self.dinamicas         = self.original[ 'dinamicas' ]
    self.alturas           = self.original[ 'alturas' ]
    self.tonos             = self.original[ 'tonos' ]
    self.voces             = self.original[ 'voces' ]
    self.capas             = self.original[ 'controles' ]

    self.bpm = self.BPMs[0]
    self.programa = self.programas[0]

  @property
  def metro( self ):
    metro = self.original[ 'metro' ].split( '/' ) 
    denominador = int( math.log10( int( metro[ 1 ] ) ) / math.log10( 2 ) )
    return {
      'numerador'        : int( metro[ 0 ] ),
      'denominador'      : denominador,
      'relojes_por_tick' : 12 * denominador,
      'notas_por_pulso'  : 8,
    }
    #return self.original[ 'metro' ].split( '/' ) 

  @property
  def fluctuacion( self ):
    fluctuacion = self.original['fluctuacion']
    rand_min = 0
    if 'min' in fluctuacion:
        rand_min = fluctuacion['min'] 
    rand_max = 0
    if 'max' in fluctuacion:
        rand_max = fluctuacion['max']
    f = random.uniform( 
        rand_min,
        rand_max 
    ) if rand_min or rand_max else 1
    return f 
    
  @property
  def articulaciones( self ):
    o = []
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
    self.cantidad_pasos = len( ganador )
    #pprint.pprint(self.referente)

    """ Consolidad "articulacion" 
    combinar parametros: altura, duracion, dinamica, etc. """
    bpm       = 0 
    programa  = 0 
    tono      = 0 
    for paso in range( self.cantidad_pasos ):
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
         id        = str( self.numero ) + self.nombre + str( paso ),
         orden     = paso,
         bpm       = self.BPMs[ paso % len( self.BPMs ) ],
         programa  = self.programas[ paso % len( self.programas ) ],
         tono      = self.tonos[ paso % len( self.tonos ) ],

         duracion  = self.duraciones[ paso % len( self.duraciones ) ],
         dinamica  = self.dinamicas[ paso % len( self.dinamicas ) ] * self.fluctuacion,
         nota      = nota,
         acorde    = acorde,
         controles = controles,
      )
      o.append( articulacion )
    return o

  """ Extrae referentes recursivamente """
  def referir(
      refs,
      o = None,
    ):
    print(refs)
    #referente   = refs[ 'referente' ]   if 'referente'   in refs else None
    #nombre      = refs[ 'nombre' ]      if 'nombre'      in refs else None
    #recurrencia = refs[ 'recurrencia' ] if 'recurrencia' in refs else None
    #nivel       = refs[ 'nivel' ]       if 'nivel'       in refs else None
    output      = o                     if o is not None         else [ None ] * nivel 
    #output[ nivel - 1 ] = ( nombre, recurrencia )
    #if referente:
    #  referir( referente, output )
    return output
  

 
