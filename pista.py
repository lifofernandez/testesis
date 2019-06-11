from argumentos import args, verboseprint, Excepcion
from segmento import Segmento
from seccion import Seccion
import random
import sys

class Pista:
  """
  Clase para cada definicion de a partir de archivos .yml
  PISTA > Secuencia > Secciones > Segmentos > Articulaciones
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
    self.numero     = Pista.cantidad 
    Pista.cantidad += 1
    Pista.defacto = Segmento(
      pista = 'defacto',
      orden = 0,
      propiedades = {
        'nombre' : 'defacto',
        **Pista.defactos
      }
    )

    self.paleta     = paleta

    self.secuencia  = [] 
    self.secuenciar( forma )
    
    verboseprint( '\n#### ' + self.nombre + ' ####' )

  """ Organiza unidades según relacion de referencia """
  def secuenciar( 
    self,
    forma    = None,
    nivel    = 0,
    herencia = {},
    seccion  = None
  ):
    nivel += 1
    """ Limpiar parametros q no se heredan.  """
    herencia.pop( 'forma', None )
    herencia.pop( 'reiterar', None )
    error = "PISTA \"" + self.nombre + "\""

    """ Recorre lista d unidades principales.  """
    cuenta_seccion = 0
    cuenta_segmentos = 0
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
          
        """ Crea parametros de unidad combinando originales con herencia """
        sucesion = {
          **original,
          **herencia,
          'nombre'      : unidad,
          'recurrencia' : recurrencia,
          'nivel'       : nivel,
        } 

        """ Cantidad de repeticiones de la unidad. """
        reiterar = 1
        if 'reiterar' in original:
          reiterar = original[ 'reiterar' ]
        for r in range( reiterar ):

          if 'forma' in original:
            """ Si esta tiene parametro "forma" es una seccio es una seccion
            refiere a otras unidades "hijas"
            crea una seccion y pasa de vuelta por esta metodo.  """

            # si HAY o NO HAY seccion
            
            # TODO agregar "seccion" de segmentos o de secciones
            seccion = Seccion(
              id = unidad,
              pista = self.nombre,
              orden = cuenta_seccion,
            )
            cuenta_seccion += 1

            self.secuenciar( 
              original[ 'forma' ],
              nivel,
              sucesion,
              seccion 
            ) 

          else: 
            """ Si esta unidad NO refiere a otra unidad = "celula" """
            segmento = Segmento(
              pista       = self.nombre,
              orden       = cuenta_segmentos,
              propiedades = {
                **Pista.defactos,
                **sucesion,
              }
            )
            cuenta_segmentos += 1

            self.secuencia.append( segmento )
            seccion.elementos.append( segmento )

            #seccion de secciones
            #self.seccion.elementos.append( seccion )

            #self.secuencia.append( seccion )
        print("SECCION",seccion)

      except Excepcion as e:
          print( e )
