import math
from .elemento import Elemento
from .articulacion import Articulacion
from .complemento import Complemento


class Segmento( Elemento ):
  """
  Secuencia > Pista > Secciones > SEGMENTOS > Articulaciones
  Conjunto de Articulaciones
  """
  cantidad = 0

  defactos = {

    # Propiedades de Segmento 
    'canal'    : 0,
    'revertir' : None,
    'NRPN'     : None,
    'RPN'      : None,

    # Props. que NO refieren a Meta Canal
    'metro'             : '4/4',
    'alteraciones'      : 0, 
    'modo'              : 0,
    'afinacionNota'     : None,
    'afinacionBanco'    : None,
    'afinacionPrograma' : None,
    'sysEx'             : None,
    'uniSysEx'          : None,

    # Procesos de Segmento
    'transportar' : 0,
    'transponer'  : 0,
    'reiterar'    : 1,

    # Propiedades de Articulacion 
    'BPMs'         : [ 60 ],
    'programas'    : [ None ],
    'duraciones'   : [ 1 ],
    'dinamicas'    : [ 1 ],
    'registracion' : [ 1 ],
    'alturas'      : [ 1 ],
    'letras'       : [ None ], 
    'tonos'        : [ 0 ],
    'voces'        : None,
    'controles'    : None,

  }

  def verbose( self, vebosidad = 0 ):
    o = self.tipo + ''
    o += str( self.numero_segmento) + '\t' 
    o += str( self ) + ' '
    o += '-' * ( 28 - (len( self.nombre ) + self.nivel))
    if vebosidad > 2:
      o +=  '\n' + ('.' * 70 )  
      o += '\n\tORD\tBPM\tDUR\tDIN\tALT\tLTR\tTON\tCTR\n' 
      for a in self.articulaciones:
        o += str( a )
    return o

  def __init__( 
    self,
    pista, 
    nombre,
    nivel,
    orden,
    recurrencia,
    referente,
    propiedades
  ):
    Elemento.__init__( 
      self,
      pista, 
      nombre,
      nivel,
      orden,
      recurrencia,
      referente
    )
    self.numero_segmento = Segmento.cantidad 
    Segmento.cantidad += 1
    self.tipo = 'SGMT'

    self.props = {
      **Segmento.defactos,
      **propiedades 
    }

    """ PRE PROCESO DE SEGMENTO """
    """ Cambia el sentido de los parametros de
    articulacion """
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
    self.transponer        = self.props[ 'transponer' ]
    self.transportar       = self.props[ 'transportar' ]
    self.alteraciones      = self.props[ 'alteraciones' ]
    self.modo              = self.props[ 'modo' ]
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
    self.letras            = self.props[ 'letras' ]
    self.tonos             = self.props[ 'tonos' ]
    self.voces             = self.props[ 'voces' ]
    self.capas             = self.props[ 'controles' ]

    self.bpm = self.BPMs[0]
    self.programa = self.programas[0]


    """ COMPLEMENTOS
        Pasar propiedades por metodos de usuario
    """
    #for complemento in self.pista.complemento:
    if self.pista.complemento:
      for metodo in dir( self.pista.complemento.modulo ):
        if metodo in self.props:
          for clave in self.props[ metodo ]:
            original = getattr( self, clave )
            argumentos = self.props[ metodo ][ clave ]
            # print( metodo, ':', clave, argumentos )
            modificado = getattr(
               self.pista.complemento.modulo, 
               metodo,
            )( original, argumentos )
            setattr( self, clave, modificado )


  @property
  def precedente( self ):
    n = self.orden
    o = self.pista.segmentos[ n - 1 ]
    return o 

  def obtener( self, key ):
      try:
        o = getattr( self, key )
        return o
      except AttributeError as e:
        return e

  def cambia(
      self,
      key
    ):
    este = self.obtener( key ) 
    anterior = self.precedente.obtener( key )
    if (
      self.orden == 0
      and este
    ):
      return True
    return anterior != este

  @property
  def tiempo( self ):
    # duracion en segundos
    return sum( [ a.tiempo for a in self.articulaciones ] ) 

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
  def clave( self ):
    return { 
      'alteraciones' : self.alteraciones,
      'modo' : self.modo
    }

  @property
  def ganador( self ):
    """ Evaluar que propiedad lista es el que mas valores tiene.  """
    self.ganador_voces = [ 0 ]
    if self.voces:
      self.ganador_voces = max( self.voces, key = len ) 
    self.ganador_capas = [ 0 ]
    if self.capas:
      self.ganador_capas = max( self.capas , key = len ) 

    candidatos = [ 
      self.dinamicas,
      self.duraciones,
      self.alturas,
      self.letras,
      self.tonos,
      self.BPMs,
      self.programas,
      self.ganador_voces,
      self.ganador_capas,
    ]
    return max( candidatos, key = len )

  @property
  def cantidad_pasos( self ):
    return len( self.ganador )

  @property
  def articulaciones( self ):

    """ Consolidar "articulacion" 
    combinar parametros: altura, duracion, dinamica, etc. """
    o = []
    for paso in range( self.cantidad_pasos ):
      """ Alturas, voz y superposición voces. """
      altura = self.alturas[ paso % len( self.alturas ) ]
      acorde = []
      nota   = altura 
      """ Relacion: altura > puntero en el set de registracion;
      Trasponer dentro del set de registracion, luego Transportar,
      sumar a la nota resultante. """
      n = self.registracion[
        ( ( altura - 1 ) + self.transponer ) % len( self.registracion )
      ] 
      nota = self.transportar + n
      """ Armar superposicion de voces. """
      if self.voces:
        for v in self.voces:
          voz = ( 
            altura + ( v[ paso % len( v ) ] )  
          ) + self.transponer
          acorde += [ 
            self.transportar + 
            self.registracion[ voz % len( self.registracion ) ] 
          ]
      """ Cambios de control. """
      controles = []
      if self.capas:
        for capa in self.capas:
          controles += [ capa[ paso % len( capa ) ] ]
      """ Articulación a secuenciar. """
      articulacion = Articulacion(
         segmento  = self,
         orden     = paso,
         bpm       = self.BPMs[ paso % len( self.BPMs ) ],
         programa  = self.programas[ paso % len( self.programas ) ],
         # TODO advertir si lista de duraciones vacias
         duracion  = self.duraciones[ paso % len( self.duraciones ) ],
         dinamica  = self.dinamicas[ paso % len( self.dinamicas ) ],
         nota      = nota,
         acorde    = acorde,
         tono      = self.tonos[ paso % len( self.tonos ) ],
         letra     = self.letras[ paso % len( self.letras ) ],
         controles = controles,
      )
      o.append( articulacion )
    return o
    
