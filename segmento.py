# TODO Agregar duracion de segmento
import random
import math
from elemento import Elemento
from articulacion import Articulacion
from argumentos import Excepcion

class Segmento( Elemento ):
  """
  Pista > Secuencia > Secciones > SEGMENTOS > Articulaciones
  Conjunto de Articulaciones
  """
  cantidad = 0

  defactos = {
    # TO DO Meta Track
    # Agrupar/Revisar/Avisar propiedades "Globales" 
    # que NO refieren a un canal en particualr
    #'addTrackName',
    #'addCopyright',

    #'addTempo',
    #'addTimeSignature',
    #'addKeySignature',
    #'changeNoteTuning',
    #'addSysEx',
    #'addUniversalSysEx',

    # Propiedades de Segmento 
    'canal'             : 1,
    'desplazar'         : 0,
    'metro'             : '4/4',
    'clave'             : { 'alteraciones' : 0, 'modo' : 0 },
    'fluctuacion'       : { 'min' : 1, 'max' : 1 },
    'transportar'       : 0,
    'transponer'        : 0,
    'reiterar'          : 1,
    'referente'         : None,
    'revertir'          : None,
    'afinacionNota'     : None,
    'afinacionBanco'    : None,
    'afinacionPrograma' : None,
    'sysEx'             : None,
    'uniSysEx'          : None,
    'NRPN'              : None,
    'RPN'               : None,

    # Propiedades de Articulacion 
    'BPMs'         : [ 60 ],
    'programas'    : [ 1 ],
    'duraciones'   : [ 1 ],
    'dinamicas'    : [ 1 ],
    'registracion'   : [ 1 ],
    'alturas'      : [ 1 ],
    'tonos'        : [ 0 ],
    'voces'        : None,
    'controles'    : None,
  }

  def __str__( self ):
    o = Elemento.__str__( self )
    o += self.tipo + ' '
    o += str( self.numero_segmento) + '\t' 
    return o  

  def __init__( 
    self,
    pista, 
    nombre,
    nivel,
    orden,
    recurrencia,
    propiedades
  ):
    Elemento.__init__( 
      self,
      pista, 
      nombre,
      nivel,
      orden,
      recurrencia
    )
    self.numero_segmento = Segmento.cantidad 
    Segmento.cantidad += 1
    self.tipo = 'SEGMENTO'
    self.props = propiedades 

    """ PRE PROCESO DE UNIDAD """
    """ Cambia el sentido de los parametros de articulacion """
    self.revertir = self.props[ 'revertir' ]
    if self.revertir:
      if isinstance( self.revertir , list ): 
        for r in self.revertir:
          if r in self.props:
            self.props[ r ].reverse() 
      elif isinstance( self.revertir , str ):
        if revertir in self.props:
          self.props[ self.revertir ].reverse() 

    self.canal             = self.props[ 'canal' ]
    self.reiterar          = self.props[ 'reiterar' ]
    self.desplazar         = self.props[ 'desplazar' ]
    self.transponer        = self.props[ 'transponer' ]
    self.transportar       = self.props[ 'transportar' ]
    self.referente         = self.props[ 'referente' ]
    self.clave             = self.props[ 'clave' ]

    self.afinacionNota     = self.props[ 'afinacionNota' ]
    self.afinacionBanco    = self.props[ 'afinacionBanco' ]
    self.afinacionPrograma = self.props[ 'afinacionPrograma' ]
    self.sysEx             = self.props[ 'sysEx' ]
    self.uniSysEx          = self.props[ 'uniSysEx' ]
    self.NRPN              = self.props[ 'NRPN' ]
    self.RPN               = self.props[ 'RPN' ]
    self.registracion      = self.props[ 'registracion' ]

    self.programas         = self.props[ 'programas' ]
    self.duraciones        = self.props[ 'duraciones' ]
    self.BPMs              = self.props[ 'BPMs' ]
    self.dinamicas         = self.props[ 'dinamicas' ]
    self.alturas           = self.props[ 'alturas' ]
    self.tonos             = self.props[ 'tonos' ]
    self.voces             = self.props[ 'voces' ]
    self.capas             = self.props[ 'controles' ]

    self.bpm = self.BPMs[0]
    self.programa = self.programas[0]

  @property
  def precedente( self ):
    n = self.orden
    # self.pista.segmentos puede ser: self.hermanos
    o = self.pista.segmentos[ n - 1]
    return o 

  def obtener( self, key ):
      try:
        o = getattr( self, key )
        return o
      except AttributeError as e:
        return e

  def cambia( self, key ):
      if self.orden == 0:
        return True
      anterior = self.precedente.obtener( key )
      este = self.obtener( key ) 
      return anterior != este

  @property
  def metro( self ):
    metro = self.props[ 'metro' ].split( '/' ) 
    denominador = int(
      math.log10( int( metro[ 1 ] ) ) / math.log10( 2 )
    )
    return {
      'numerador'        : int( metro[ 0 ] ),
      'denominador'      : denominador,
      'relojes_por_tick' : 12 * denominador,
      'notas_por_pulso'  : 8,
    }

  @property
  def fluctuacion( self ):
    fluctuacion = self.props['fluctuacion']
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
         #id        = str( self.numero ) + self.nombre + str( paso ),
         segmento  = self,
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
    #print(refs)
    #referente   = refs[ 'referente' ]   if 'referente'   in refs else None
    #nombre      = refs[ 'nombre' ]      if 'nombre'      in refs else None
    #recurrencia = refs[ 'recurrencia' ] if 'recurrencia' in refs else None
    #nivel       = refs[ 'nivel' ]       if 'nivel'       in refs else None
    output      = o                     if o is not None         else [ None ] * nivel 
    #output[ nivel - 1 ] = ( nombre, recurrencia )
    #if referente:
    #  referir( referente, output )
    return output
  

 
