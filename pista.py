from argumentos import args, verboseprint, Excepcion
from segmento import Segmento
#from secuencia import Secuencia
import random
import sys

class Pista:
  """
  Clase para cada definicion de a partir de archivos .yml
  PISTA > Secuencia > Segmentos > Articulaciones
  """
  cantidad = 0 
  defactos = {

    # TO DO 
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
    o = '' 
    for attr, value in self.__dict__.items():
      l = str( attr ) + ':' + str( value )
      o += l + '\n'
    return o
 
  def __init__( 
    self,
    nombre,
    paleta,
    forma
  ):
    self.nombre     = nombre
    self.orden      = Pista.cantidad 
    Pista.cantidad += 1
    Pista.defacto = Segmento(
      nombre,
      {
        'nombre' : 'defacto',
        **Pista.defactos
      }
    )

    self.paleta     = paleta
    self.registros  = {}

    self.secuencia  = [] 
    self.secuenciar( forma )
    
    verboseprint( '\n#### ' + self.nombre + ' ####' )

  """ Organiza unidades según relacion de referencia """
  def secuenciar( 
    self,
    forma    = None,
    nivel    = 0,
    herencia = {},
  ):
    nivel += 1
    """ Limpiar parametros q no se heredan.  """
    herencia.pop( 'forma', None )
    herencia.pop( 'reiterar', None )
    error = "PISTA \"" + self.nombre + "\""
    """ Recorre lista ordenada unidades principales.  """
    for unidad in forma:  
      verboseprint( '-' * ( nivel - 1 ) +  unidad )
      try:
        if unidad not in self.paleta:
          error += " NO ENCUENTRO \"" + unidad + "\"  "  
          raise Excepcion( unidad, error )
          pass
        original = self.paleta[ unidad ]
        """ Cuenta recurrencias de esta unidad en este nivel.  """
        recurrencia = 0
        if nivel in self.registros:
          # TODO Que los cuente en cualquier nivel.
          recurrencia = sum( 
            [ 1 for r in self.registros[ nivel ] if r[ 'nombre' ] == unidad ]
          ) 
        """ Dicionario para ingresar al arbol de registros.
        Si el referente está en el diccionario herencia registrar
        referente.  """
        registro = { 
          'nombre'      : unidad,
          'recurrencia' : recurrencia,
          'nivel'       : nivel,
        }
        if 'referente' in herencia:
          registro[ 'referente' ] = herencia[ 'referente' ] 
        """ Crea parametros de unidad combinando originales con herencia
        Tambien agrega el registro de referentes """
        sucesion = {
          **original,
          **herencia,
          **registro # separar esto
        } 
        """ Cantidad de repeticiones de la unidad.  """
        reiterar = 1
        if 'reiterar' in original:
          reiterar = original[ 'reiterar' ]
        for r in range( reiterar ):
          """ Agregar a los registros """
          self.registros.setdefault( nivel , [] ).append( registro )
          if 'forma' in original:
            """ Si esta tiene parametro "unidades", refiere a otras unidades
            "hijas" pasa de vuelta por esta metodo.  """
            sucesion[ 'referente' ] = registro 
            self.secuenciar( 
              original[ 'forma' ],
              nivel,
              sucesion,
            ) 
          else: 
            """ Si esta unidad no refiere a otra unidade = "celula" 
            Combinar "defactos" con: resultado de original + sucesion. """
            resultante = {
              **Pista.defactos,
              **sucesion,
            }
            """ Generar Segmento y adjuntar a la secuencia """
            segmento = Segmento(
              self.nombre,
              resultante
            )
            self.secuencia.append( segmento )
      except Excepcion as e:
          print( e )
