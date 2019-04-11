from argumentos import args, verboseprint
import random
import sys

class Pista:
  """
  Clase para cada 'track' a partir de archivos.yml
  """
  cantidad = 0 
  defactos = {
    'bpm'           : 60,
    'canal'         : 1,
    'programa'      : 1,
    'metro'         : '4/4',
    'alturas'       : [ 1 ],
    'clave'         : { 'alteraciones' : 0, 'modo' : 0 },
    'intervalos'    : [ 1 ],
    'voces'         : None,
    'duraciones'    : [ 1 ],
    'desplazar'     : 0,
    'dinamicas'     : [ 1 ],
    'fluctuacion'   : { 'min' : 1, 'max' : 1 },
    'transportar'   : 0,
    'transponer'    : 0,
    #'controles'     : [ [ None ] ],
    'controles'     : None,
    'reiterar'      : 1,
    'referente'     : None,
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
    #self.oid        = str( self.orden ) + self.nombre 
    """
    Parametros defactos de unidadad llamados "base"
    """
    #self.base       = base
    #self.duracion   = 0
    """
    Principal Lista ordenada de unidades "macroforma"
    """
    self.macroforma = macroforma
    """
    A partir de esa lista busca en la "paleta de unidades"
    """
    self.paleta     = paleta

    self.registros  = {}
    self.secuencia  = [] 
    self.ordenar()
    #self.secuencia = self.ordenar( macroforma )
    #pprint.pprint( self.registros )

    verboseprint( '\n#### ' + self.nombre + ' ####' )

  def __str__( self ):
    o = '' 
    for attr, value in self.__dict__.items():
      l = str( attr ) + ':' + str( value )
      o += l + '\n'
    return o

  def ordenar( 
    self,
    forma    = None,
    nivel    = 0,
    herencia = {},
  ):
    """
    Organiza unidades según relacion de referencia
    """
    forma = forma if forma is not None else self.macroforma
    nivel += 1
    """
    Limpiar parametros q no se heredan
    """
    herencia.pop( 'unidades', None )
    herencia.pop( 'reiterar', None )

    for unidad in forma:  
      verboseprint( '-' * ( nivel - 1 ) +  unidad )
      """
      Si esta tratando de invocar una unidad que no disponible en la paleta de unidades
      """
      try:
        #if unidad in self.paleta:
        """
        Carga unidad original 
        """
        unidad_objeto = self.paleta[ unidad ]
        """
        Cuenta recurrencias de esta unidad en este nivel
        """
        recurrencia = sum( 
          [ 1 for r in self.registros[ nivel ] if r[ 'nombre' ] == unidad ]
        ) if nivel in self.registros else 0 
        """
        Dicionario para ingresar al arbol de registros
        """
        registro = { 
          'nombre'      : unidad,
          'recurrencia' : recurrencia,
          'nivel'       : nivel,
        }

        """
        Si el referente esta herencia registrar refernete
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
        Cantidad de repeticiones de la unidad
        """
        reiterar = unidad_objeto[ 'reiterar' ] if 'reiterar' in unidad_objeto else 1
        # n = str( nivel ) + unidad + str( recurrencia )
        for r in range( reiterar ):
          self.registros.setdefault( nivel , [] ).append( registro )

          if 'unidades' in unidad_objeto:
            """
            Si esta refiere a otras pasar de vuelta por esta funcion
            """
            sucesion[ 'referente' ] = registro 
            self.ordenar( 
              unidad_objeto[ 'unidades' ],
              nivel,
              sucesion,
            ) 

          else: 
            """
            Si esta unidad no refiere a otra unidades:
            """
            #self.registros.setdefault( 'copa' , [] ).append( registro )
            """
            Sobrescribir propiedas de unidad por "herencia"
            """
            factura = {
              **Pista.defactos,
              **sucesion,
            }
            """
            Secuenciar articulaciones
            """
            self.secuencia += self.secuenciar( factura ) 
      except:
        print("[NOTICE] No existe unidad: " + unidad )

  def secuenciar( 
    self,
    unidad
  ):
    """
    Genera una secuencia de ariculaciones musicales 
    a partir de relacion de unidades ya analizada.  
    """

    """
    Revierte parametros del tipo lista
    TODO: comvertir en lista, si es string
    """
    revertir = unidad[ 'revertir' ] if 'revertir' in unidad else None 
    if isinstance( revertir , list ): 
      for r in revertir:
        if r in unidad:
          unidad[ r ].reverse() 
    elif isinstance( revertir , str ):
      if revertir in unidad:
        unidad[ revertir ].reverse() 

    """
    Carga parametros
    """
    intervalos = unidad[ 'intervalos' ]
    alturas    = unidad[ 'alturas' ]
    voces      = unidad[ 'voces' ]
    duraciones = unidad[ 'duraciones' ]
    dinamicas  = unidad[ 'dinamicas' ]
    capas      = unidad[ 'controles' ]
    """
    Evalua que parametro es que mas valores tiene
    TODO: q cuente cuantas voces/controles es el mas largo
    """
    candidatos = [ 
      dinamicas,
      duraciones,
      alturas,
      #len(max(voces, key = len)),
      #len(max(capas, key = len)),
    ]
    ganador = max( candidatos, key = len )

    pasos = len( ganador )

    secuencia = []
    for paso in range( pasos ):
      """
      Consolidad "articulacion" a partir de combinar parametros: altura, duracion, dinamica, etc
      """
      duracion = duraciones[ paso % len( duraciones ) ]
      """
      Variaciones de dinamica
      """
      rand_min = unidad['fluctuacion']['min'] if 'min' in unidad[ 'fluctuacion' ] else None
      rand_max = unidad['fluctuacion']['max'] if 'max' in unidad[ 'fluctuacion' ] else None
      fluctuacion = random.uniform( 
         rand_min,
         rand_max 
      ) if rand_min or rand_max else 1
      """
      Asignar una dinámica
      """
      dinamica = dinamicas[ paso % len( dinamicas ) ] * fluctuacion
      """
      Alturas y voces
      """
      altura = alturas[ paso % len( alturas ) ]
      acorde = []
      nota = 'S' # Silencio
      """
      Si tiene una "altura"
      """
      if altura != 0:
        """
        Relacion: altura > puntero en el set de intervalos
        Trasponer dentro del set de intervalos despues de 
        Transportar, sumar al intervalo 
        """
        transponer  = unidad[ 'transponer' ] 
        transportar = unidad[ 'transportar' ]
        nota = transportar + intervalos[ ( ( altura - 1 ) + transponer ) % len( intervalos ) ] 
        """
        Armar superposicion de voces
        """
        if voces:
          for v in voces:
            voz = ( altura + ( v[ paso % len( v ) ] ) - 1 ) + transponer
            acorde += [ transportar +  intervalos[ voz % len( intervalos ) ]  ]

      """
      Cambios de control
      """
      controles = []
      if capas:
        for capa in capas:
          controles += [ capa[ paso % len( capa ) ] ]

      """
      Articulación a secuenciar
      """
      articulacion = {
        **unidad, # Pasa algunas cosas de mas aca...
        'unidad'      : unidad[ 'nombre' ],
        'orden'       : paso,
        'altura'      : nota,
        'acorde'      : acorde,
        'duracion'    : duracion,
        'dinamica'    : dinamica,
        'controles'   : controles,
      }
      secuencia.append( articulacion )
    return secuencia 


#def linux_interaction():
#    assert ('linux' in sys.platform), "Function can only run on Linux systems."
#    print('Doing something.')
#
#try:
#    linux_interaction()
#except:
#    pass
