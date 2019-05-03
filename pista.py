from argumentos import args, verboseprint, Excepcion
from segmento import Segmento
import random
import sys

class Pista:
  """
  Clase para cada definicion de a partir de archivos .yml
  YAML => Pista => Canal 
  """
  cantidad = 0 
  defactos = {
    'bpm'               : 60,
    'canal'             : 1,
    'programa'          : 1,
    'metro'             : '4/4',
    'alturas'           : [ 1 ],
    'tonos'             : [ 0 ],
    'clave'             : { 'alteraciones' : 0, 'modo' : 0 },
    'intervalos'        : [ 1 ],
    'voces'             : None,
    'duraciones'        : [ 1 ],
    'desplazar'         : 0,
    'dinamicas'         : [ 1 ],
    'fluctuacion'       : { 'min' : 1, 'max' : 1 },
    'transportar'       : 0,
    'transponer'        : 0,
    'controles'         : None,

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
  }
 
  def __init__( 
    self,
    nombre,
    paleta,
    macroforma,
  ):
    self.nombre     = nombre
    self.orden      = Pista.cantidad 
    Pista.cantidad += 1

    self.macroforma = macroforma
    self.paleta     = paleta
    self.registros  = {}
    self.secuencia  = [] 
    self.SECUENCIA  = [] 
    self.ordenar()

    #self.oid        = str( self.orden ) + self.nombre 
    #self.duracion   = 0
    #self.secuencia  = self.ordenar( macroforma )

    verboseprint( '\n#### ' + self.nombre + ' ####' )

  def __str__( self ):
    o = '' 
    for attr, value in self.__dict__.items():
      l = str( attr ) + ':' + str( value )
      o += l + '\n'
    return o

  """
  Organiza unidades según relacion de referencia
  """
  def ordenar( 
    self,
    forma    = None,
    nivel    = 0,
    herencia = {},
  ):
    forma = forma if forma is not None else self.macroforma
    nivel += 1
    """
    Limpiar parametros q no se heredan.
    """
    herencia.pop( 'unidades', None )
    herencia.pop( 'reiterar', None )

    """
    Recorre lista ordenada unidades principales.
    """
    error =  "PISTA \"" + self.nombre + "\""
    for unidad in forma:  
      verboseprint( '-' * ( nivel - 1 ) +  unidad )
      try:
        if unidad not in self.paleta:
          error +=  " NO ENCUENTRO \"" + unidad + "\"  "  
          raise Excepcion( unidad, error )
          pass
        unidad_objeto = self.paleta[ unidad ]
        """
        Cuenta recurrencias de esta unidad en este nivel.
        TODO: Que los cuente en cualquier nivel.
        """
        recurrencia = sum( 
          [ 1 for r in self.registros[ nivel ] if r[ 'nombre' ] == unidad ]
        ) if nivel in self.registros else 0 
        """
        Dicionario para ingresar al arbol de registros.
        """
        registro = { 
          'nombre'      : unidad,
          'recurrencia' : recurrencia,
          'nivel'       : nivel,
        }

        """
        Si el referente está en el diccionario herencia registrar referente.
        """
        if 'referente' in herencia:
          registro[ 'referente' ] = herencia[ 'referente' ] 

        """
        Crea parametros de unidad combinando originales con herencia
        Tambien agrega el registro de referentes
        """
        sucesion = {
          **unidad_objeto,
          **herencia,
          **registro
        } 
        """
        Cantidad de repeticiones de la unidad.
        """
        reiterar = unidad_objeto[ 'reiterar' ] if 'reiterar' in unidad_objeto else 1
        # n = str( nivel ) + unidad + str( reiterar )
        for r in range( reiterar ):
          self.registros.setdefault( nivel , [] ).append( registro )

          if 'unidades' in unidad_objeto:
            """
            Si esta tiene parametro "unidades", refiere a otras unidades "hijas" 
            pasa de vuelta por esta metodo.
            """
            sucesion[ 'referente' ] = registro 
            self.ordenar( 
              unidad_objeto[ 'unidades' ],
              nivel,
              sucesion,
            ) 
          else: 
            """
            Si esta unidad no refiere a otra unidades, 
            Unidad célula 
            """
            """
            Combinar "defactos" con propiedas resultantes de unidad + "herencia" y registro.
            """
            factura = {
              **Pista.defactos,
              **sucesion,
            }
            """
            Secuenciar articulaciones
            """
            self.secuencia += self.secuenciar( factura ) 
      except Excepcion as e:
          print(e)


  """
  Genera una secuencia de ariculaciones musicales 
  a partir de unidades preprocesadas. 
  """
  def secuenciar( 
    self,
    unidad
  ):


    SECUENCIA = []
    ARTICULACIONES = []

    ## ARMAR SEGMENTO
    segmento = Segmento(
      unidad[ 'nombre' ],
    )

    segmento.reiterar = unidad[ 'reiterar' ]
    segmento.revertir = unidad[ 'revertir' ]
    segmento.desplazar = unidad[ 'desplazar' ]
    segmento.referente = unidad[ 'referente' ]
    segmento.afinacionNota = unidad[ 'afinacionNota' ]
    segmento.afinacionBanco = unidad[ 'afinacionBanco' ]
    segmento.afinacionPrograma = unidad[ 'afinacionPrograma' ]
    segmento.sysEx = unidad[ 'sysEx' ]
    segmento.uniSysEx = unidad[ 'uniSysEx' ]
    segmento.NRPN = unidad[ 'NRPN' ]
    segmento.RPN = unidad[ 'RPN' ]

    ## AGREGAR PROPS DE SEGMENTO

    ## ENCHUFAR ARTICULACIONES AL SEGUNEMTO
    ## AGREGAR 

    """
    Cambia el sentido de los parametros del tipo lista
    TODO: ¿convertir cualquier string o int en lista?
    """
    if 'revertir' in unidad:
      revertir = unidad[ 'revertir' ] 
      if isinstance( revertir , list ): 
        for r in revertir:
          if r in unidad:
            unidad[ r ].reverse() 
      elif isinstance( revertir , str ):
        if revertir in unidad:
          unidad[ revertir ].reverse() 

    intervalos    = unidad[ 'intervalos' ]
    duraciones    = unidad[ 'duraciones' ]
    dinamicas     = unidad[ 'dinamicas' ]
    alturas       = unidad[ 'alturas' ]
    tonos         = unidad[ 'tonos' ]
    voces         = unidad[ 'voces' ]
    ganador_voces = max( voces, key = len) if voces else [ 0 ]
    capas         = unidad[ 'controles' ]
    ganador_capas = max( capas , key = len) if capas else [ 0 ]

    """
    Evaluar que parametro lista es el que mas valores tiene.
    """
    candidatos = [ 
      dinamicas,
      duraciones,
      alturas,
      ganador_voces,
      ganador_capas,
      tonos,
    ]
    ganador = max( candidatos, key = len )
    pasos = len( ganador )
    secuencia = []

    """
    Consolidad "articulacion" 
    combinar parametros: altura, duracion, dinamica, etc.
    """
    for paso in range( pasos ):
      duracion = duraciones[ paso % len( duraciones ) ]
      """
      Variaciones de dinámica.
      """
      if 'min' in unidad[ 'fluctuacion' ]:
        rand_min = unidad['fluctuacion']['min'] 
      if 'max' in unidad[ 'fluctuacion' ]:
        rand_max = unidad['fluctuacion']['max']
      fluctuacion = random.uniform( 
         rand_min,
         rand_max 
      ) if rand_min or rand_max else 1
      """
      Asignar dinámica.
      """
      dinamica = dinamicas[ paso % len( dinamicas ) ] * fluctuacion
      """
      Alturas, voz y superposición voces.
      """
      altura = alturas[ paso % len( alturas ) ]
      tono   = tonos[ paso % len( tonos ) ]
      acorde = []
      nota = 'S' # Silencio
      if altura != 0:
        """
        Relacion: altura > puntero en el set de intervalos; Trasponer dentro
        del set de intervalos, luego Transportar, sumar a la nota resultante.
        """
        transponer  = unidad[ 'transponer' ] 
        transportar = unidad[ 'transportar' ]
        n = intervalos[ ( ( altura - 1 ) + transponer ) % len( intervalos ) ] 
        nota = transportar + n
        """
        Armar superposicion de voces.
        """
        if voces:
          for v in voces:
            voz = ( altura + ( v[ paso % len( v ) ] ) - 1 ) + transponer
            acorde += [ transportar +  intervalos[ voz % len( intervalos ) ]  ]

      """
      Cambios de control.
      """
      controles = []
      if capas:
        for capa in capas:
          controles += [ capa[ paso % len( capa ) ] ]


      """
      Articulación a secuenciar.
      """
      articulacion = {
        'desplazar'         : unidad[ 'desplazar' ],
        'referente'         : unidad[ 'referente' ],
        'afinacionNota'     : unidad[ 'afinacionNota' ],
        'afinacionBanco'    : unidad[ 'afinacionBanco' ],
        'afinacionPrograma' : unidad[ 'afinacionPrograma' ],
        'sysEx'             : unidad[ 'sysEx' ],
        'uniSysEx'          : unidad[ 'uniSysEx' ],
        'NRPN'              : unidad[ 'NRPN' ],
        'RPN'               : unidad[ 'RPN' ],

        'unidad'            : unidad[ 'nombre' ],
        'canal'             : unidad[ 'canal' ],
        'bpm'               : unidad[ 'bpm' ],
        'metro'             : unidad[ 'metro' ],
        'clave'             : unidad[ 'clave' ],
        'programa'          : unidad[ 'programa' ],
        'orden'             : paso,
        'altura'            : nota,
        'tono'              : tono,
        'acorde'            : acorde,
        'duracion'          : duracion,
        'dinamica'          : dinamica,
        'controles'         : controles,
      }
      secuencia.append( articulacion )
      ARTICULACIONES.append( articulacion )

    segmento.articulaciones = ARTICULACIONES
    print(segmento)
    SECUENCIA.append( segmento )

    return secuencia
