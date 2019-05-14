from argumentos import args, verboseprint, Excepcion
from segmento import Segmento
from secuencia import Secuencia
import random
import sys

class Pista:
  """
  Clase para cada definicion de a partir de archivos .yml
  YAML => Pista => Canal 
  """
  cantidad = 0 
  defactos = {

    # Propiedades de Segmento
    'canal'             :  1 ,
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
    'instrumentos' : [ 1 ],
    'duraciones'   : [ 1 ],
    'dinamicas'    : [ 1 ],
    'intervalos'   : [ 1 ],
    'alturas'      : [ 1 ],
    'tonos'        : [ 0 ],
    'voces'        : None,
    'controles'    : None,
  }

  """ TO DO 
  Agrupar/Revisar/Avisar propiedades "Globales" 
  que NO refieren a un canal en particualr
  'addTrackName',
  'addCopyright',
  'addTempo',
  'addTimeSignature',
  'addKeySignature',
  'changeNoteTuning',
  'addSysEx',
  'addUniversalSysEx',
  """
 
  def __init__( 
    self,
    nombre,
    paleta,
    forma,
  ):
    self.nombre     = nombre
    self.orden      = Pista.cantidad 
    Pista.cantidad += 1

    self.paleta     = paleta
    self.registros  = {}

    self.secuencia  = [] 

    self.generar_secuencia( forma )


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
  def generar_secuencia( 
    self,
    forma    = None,
    nivel    = 0,
    herencia = {},
    sequ = [],
  ):
    #forma = forma if forma is not None else self._macroforma
    #if not forma:
    #  forma = self._macroforma

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
        original = self.paleta[ unidad ]

        """
        Cuenta recurrencias de esta unidad en este nivel.
        """
        recurrencia = 0
        if nivel in self.registros:
          #TODO Revisar
          # Que los cuente en cualquier nivel.
          # puede revisar valor del anterior
          recurrencia = sum( 
            [ 1 for r in self.registros[ nivel ] if r[ 'nombre' ] == unidad ]
          ) 
        """
        Dicionario para ingresar al arbol de registros.
        Si el referente está en el diccionario herencia registrar
        referente.
        """
        registro = { 
          'nombre'      : unidad,
          'recurrencia' : recurrencia,
          'nivel'       : nivel,
        }
        #if 'referente' in herencia:
        #  #aca registrar solo nombre? 
        #  registro[ 'referente' ] = herencia[ 'referente' ] 

        """
        Crea parametros de unidad combinando originales con herencia
        Tambien agrega el registro de referentes
        """
        sucesion = {
          **original,
          **herencia,
          **registro # separar esto
        } 
        """
        Cantidad de repeticiones de la unidad.
        """
        reiterar = 1
        if 'reiterar' in original:
          reiterar = original[ 'reiterar' ]
        # n = str( nivel ) + unidad + str( reiterar )

        for r in range( reiterar ):

          """ Agregar a los registros """
          self.registros.setdefault( nivel , [] ).append( registro )

          if 'unidades' in original:
            """
            Si esta tiene parametro "unidades", refiere a otras unidades
            "hijas" pasa de vuelta por esta metodo.
            """
            sucesion[ 'referente' ] = registro 
            self.generar_secuencia( 
              original[ 'unidades' ],
              nivel,
              sucesion,
              sequ,
            ) 
          else: 
            """
            Si esta unidad no refiere a otra unidades, 
            Unidad célula 
            Combinar "defactos" con propiedas resultantes de unidad +
            "herencia" y registro.
            """
            resultante = {
              **Pista.defactos,
              **sucesion,
            }
            """
            Secuenciar articulaciones
            """
            self.secuencia += self.generar_segmento( resultante ) 
      except Excepcion as e:
          print( e )

  """
  Genera una secuencia de ariculaciones musicales 
  a partir de unidades preprocesadas. 
  """
  # metodo de Segmento? Secuencia?
  def generar_segmento( 
    self,
    unidad
  ):
    SECUENCIA = []

    """
    PRE PROCESO DE UNIDAD
    REVERTIR
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

    #pp = Secuencia( unidad )
    #print(pp)

    segmento = Segmento(
      nombre            = unidad[ 'nombre' ],
      canal             = unidad[ 'canal' ],
      reiterar          = unidad[ 'reiterar' ],
      revertir          = unidad[ 'revertir' ],
      desplazar         = unidad[ 'desplazar' ],
      transponer        = unidad[ 'transponer' ],
      transportar       = unidad[ 'transportar' ],
      referente         = unidad[ 'referente' ],
      clave             = unidad[ 'clave' ],
      metro             = unidad[ 'metro' ],
      afinacionNota     = unidad[ 'afinacionNota' ],
      afinacionBanco    = unidad[ 'afinacionBanco' ],
      afinacionPrograma = unidad[ 'afinacionPrograma' ],
      sysEx             = unidad[ 'sysEx' ],
      uniSysEx          = unidad[ 'uniSysEx' ],
      NRPN              = unidad[ 'NRPN' ],
      RPN               = unidad[ 'RPN' ],
      intervalos        = unidad[ 'intervalos' ],
      programas         = unidad[ 'programas' ],
      duraciones        = unidad[ 'duraciones' ],
      BPMs              = unidad[ 'BPMs' ],
      dinamicas         = unidad[ 'dinamicas' ],
      fluctuacion       = unidad[ 'fluctuacion' ],
      alturas           = unidad[ 'alturas' ],
      tonos             = unidad[ 'tonos' ],
      voces             = unidad[ 'voces' ],
      capas             = unidad[ 'controles' ],
    )
    SECUENCIA.append( segmento )
    return SECUENCIA

