import random
import math
from elemento import Elemento
from articulacion import Articulacion

class Segmento( Elemento ):
  """
  Pista > Secuencia > Secciones > SEGMENTOS > Articulaciones
  Conjunto de Articulaciones
  """
  cantidad = 0

  defactos = {

    # Propiedades de Segmento 
    'canal'             : 1,
    'revertir'          : None,
    'referente'         : None,

    'NRPN'              : None,
    'RPN'               : None,

    # Parametros que NO son de Canal
    # Deberian ir a META track?
    'metro'             : '4/4',
    'clave'             : { 'alteraciones' : 0, 'modo' : 0 },
    'afinacionNota'     : None,
    'afinacionBanco'    : None,
    'afinacionPrograma' : None,
    'sysEx'             : None,
    'uniSysEx'          : None,


    # Procesos de Segmento
    'transportar'       : 0,
    'transponer'        : 0,
    'reiterar'          : 1,
    'desplazar'         : 0, # ¿momento?
    'fluctuacion'       : { 'min' : 1, 'max' : 1 },

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

  def verbose( self, verbose = 0 ):
    o = self.tipo + ' '
    o += str( self.numero_segmento) + '\t' 
    o += str( self ) + ' '
    o += '-' * ( 18 - (len( self.nombre ) + self.nivel))
    if verbose > 2:
      o += '\nARTICULACIONES\n'
      o += '#\tord\tbpm\tdur\tdin\talt\tltr\tton\tctrs\n' 
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
    self.tipo = 'SGMT'
    self.props = {
        **Segmento.defactos,
        **propiedades 
    }
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
    self.letras            = self.props[ 'letras' ]
    self.tonos             = self.props[ 'tonos' ]
    self.voces             = self.props[ 'voces' ]
    self.capas             = self.props[ 'controles' ]

    self.bpm = self.BPMs[0]
    self.programa = self.programas[0]

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

  def cambia( self, key ):
      este = self.obtener( key ) 
      anterior = self.precedente.obtener( key )
      #if este:
      #  return anterior != este
      if (
        self.orden == 0
        #and este
      ):
        return True
      return anterior != este

  @property
  def duracion( self ):
    return sum(self.duraciones) 

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
      self.letras,
      self.tonos,
      self.BPMs,
      self.programas,
      self.ganador_voces,
      self.ganador_capas,
    ]
    ganador = max( candidatos, key = len )
    self.cantidad_pasos = len( ganador )

    """ Consolidar "articulacion" 
    combinar parametros: altura, duracion, dinamica, etc. """
    for paso in range( self.cantidad_pasos ):
      """ Alturas, voz y superposición voces. """
      altura = self.alturas[ paso % len( self.alturas ) ]
      acorde = []
      #nota   = 'S' # Silencio
      nota   = altura 
      #if altura:
      """ Relacion: altura > puntero en el set de registracion;
      Trasponer dentro del set de registracion, luego Transportar,
      sumar a la nota resultante. """
      n = self.registracion[
        ( ( altura - 1 ) + self.transponer ) % len( self.registracion )
      ] 
      nota = self.transportar + n
      #silencio = False
      #if altura == 0:
      #  silencio = True 
      """ Armar superposicion de voces. """
      if self.voces:
        for v in self.voces:
          voz = ( altura + ( v[ paso % len( v ) ] ) - 1 ) + self.transponer
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

         duracion  = self.duraciones[ paso % len( self.duraciones ) ],
         #paSAR DINAMICA A PROCESOS DE SEGMENTO,
         #QUE OPERE EN EL RESULTADO DE LASARTICULACIONES
         dinamica  = self.dinamicas[ paso % len( self.dinamicas ) ] * self.fluctuacion,
         nota      = nota,
         acorde    = acorde,
         #silencio  = silencio,
         tono      = self.tonos[ paso % len( self.tonos ) ],
         letra     = self.letras[ paso % len( self.letras ) ],
         controles = controles,
      )
      o.append( articulacion )
    return o

