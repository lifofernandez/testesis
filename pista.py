from argumentos import args, verboseprint
import random

# VOLAR DE ACA
if args.plot:
  print( '#### CARGANDO libs ####' )
  import matplotlib.pyplot as plt
  import numpy as np
  import matplotlib.dates as mdates
  from datetime import datetime, timedelta

class Pista:
  """
  Clase para cada 'track' a partir de archivos.yml
  """
  cantidad = 0 
  defactos = {
    'bpm'           : 60,
    'canal'         : 1,
    'programa'      : None,
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
    'controladores' : [ None ],
    'reiterar'      : 1,
    'referente'     : None,
  }
 
  def __init__( 
    self,
    nombre,
    base,
    paleta,
    macroforma,
  ):
    self.nombre = nombre
    self.orden = Pista.cantidad 
    Pista.cantidad += 1
    self.oid = str( self.orden ) + self.nombre 
    self.base = base
    self.duracion = 0
    self.paleta = paleta # paleta de unidades
    self.macroforma = macroforma

    self.registros = {}
    self.secuencia = [] 
    self.ordenar()
    #self.secuencia = self.ordenar( macroforma )
    #pprint.pprint( self.registros )

    if args.plot:
      print( '#### crear grafico ####' )
      self.fig, self.ax = plt.subplots( figsize = ( 8, 5 ) )

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
    herencia.pop( 'unidades', None )
    herencia.pop( 'reiterar', None )

    for u in forma:  
      verboseprint( '-' * ( nivel - 1 ) +  u  )

      if u in self.paleta:
        uo = self.paleta[ u ]
        # TODO q cuente recurrencias en diferentes niveles
        recurrencia = sum( 
          [ 1 for o in self.registros[ nivel ] if o[ 'nombre' ] == u ]
        ) if nivel in self.registros else 0 
        registro = { 
          'nombre'      : u,
          'recurrencia' : recurrencia,
          'nivel'       : nivel,
        }

        if 'referente' in herencia:
          registro[ 'referente' ] = herencia[ 'referente' ] 
        sucesion = {
          **uo,
          **herencia,
          **registro
        } 
        reiterar = uo[ 'reiterar' ] if 'reiterar' in uo else 0
        n = str( nivel ) + u + str( recurrencia )

        for r in range( reiterar + 1 ):
          self.registros.setdefault( nivel , [] ).append( registro )

          if 'unidades' in uo:
            sucesion[ 'referente' ] = registro 
            self.ordenar( 
              uo[ 'unidades' ],
              nivel,
              sucesion,
            ) 

          else: 
            #self.registros.setdefault( 'copa' , [] ).append( registro )
            factura = {
              **Pista.defactos,
              **sucesion,
            }
            o = self.secuenciar( factura ) 
            self.secuencia += o  

  def secuenciar( 
    self,
    unidad
  ):
    """
    Genera una secuencia de eventos a partir de unidades preprocesadas
    """
    revertir = unidad[ 'revertir' ] if 'revertir' in unidad else None 

    if isinstance( revertir , list ): 
      for r in revertir:
        if r in unidad:
          unidad[ r ].reverse() 
    elif isinstance( revertir , str ):
      if revertir in unidad:
        unidad[ revertir ].reverse() 

    intervalos    = unidad[ 'intervalos' ]
    alturas       = unidad[ 'alturas' ]
    voces         = unidad[ 'voces' ]
    duraciones    = unidad[ 'duraciones' ]
    dinamicas     = unidad[ 'dinamicas' ]
    controladores = unidad[ 'controladores' ]
    candidatos = [ 
      dinamicas,
      duraciones,
      alturas,
      controladores,
    ]
    ganador = max( candidatos, key = len )
    pasos = len( ganador )
    seq = []

    for paso in range( pasos ):
      """
      Combinar parametros: altura, duracion, dinamica, etc
      """
      duracion = duraciones[ paso % len( duraciones ) ]
      rand_min = unidad['fluctuacion']['min'] if 'min' in unidad[ 'fluctuacion' ] else None
      rand_max = unidad['fluctuacion']['max'] if 'max' in unidad[ 'fluctuacion' ] else None
      fluctuacion = random.uniform( 
         rand_min,
         rand_max 
      ) if rand_min or rand_max else 1
      dinamica = dinamicas[ paso % len( dinamicas ) ] * fluctuacion
      controlador = controladores[ paso % len( controladores ) ]
      altura = alturas[ paso % len( alturas ) ]
      acorde = []
      nota = 'S' # Silencio

      if altura != 0:
        """
        altura / puntero intervalo
        """
        transponer  = unidad[ 'transponer' ] 
        transportar = unidad[ 'transportar' ]
        nota = transportar + intervalos[ ( ( altura - 1 ) + transponer ) % len( intervalos ) ] 
        if voces:
          for v in voces:
            voz = ( altura + ( v[ paso % len( v ) ] ) - 1 ) + transponer
            acorde += [ transportar +  intervalos[ voz % len( intervalos ) ]  ]
      evento = {
        **unidad, #TODO pasa mucha cosa de mas aca
        'unidad'      : unidad[ 'nombre' ],
        'orden'       : paso,
        'altura'      : nota,
        'acorde'      : acorde,
        'duracion'    : duracion,
        'dinamica'    : dinamica,
        'controlador' : controlador,
      }
      seq.append( evento )
    return seq 

