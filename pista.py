from argumentos import args, verbose, Excepcion
import pprint
from elemento import Elemento
from seccion  import Seccion
from segmento import Segmento

#from elemento import Elemento, Seccion, Segmento

import random
import sys

class Pista:
  """
  Clase para cada definicion de a partir de archivos .yml
  PISTA > Secuencia > Secciones > Segmentos > Articulaciones
  """
  cantidad = 0 

  def __str__( self ):
    # Esto es para verbose print level 1
    o = 'PISTA ' + str( self.numero) + ': '+ str( self.nombre  )

    # Esto es para verbose print level 2
    o +=  '\n#\torden\tnivel\trecur\tnombre\n'
    for e in self.elementos:
      o += str(e) + '\n'
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
    self.paleta = paleta
    self.forma = forma 

    # hacer uno para todas las pistas
    # Segmento 0, inicial sacar de la cuenta general
    # puede heredar de 'base'
    #Pista.defacto = Segmento(
    #  pista = self,
    #  nombre = 'Segmento Inicial',
    #  nivel = None,
    #  orden = None,
    #  recurrencia = None,
    #  propiedades = {
    #    **Segmento.defactos
    #  }
    #)

    self.secciones = []
    self.segmentos = []
    self.seccionar( self.forma )

  @property
  def elementos( self ):
    return sorted( 
      self.secciones + self.segmentos,
      key=lambda x: x.numero
    )

  #@property
  def precedente( self, n  ):
    return self.segmentos[ n - 1]

  """ Organiza unidades según relacion de referencia """
  def seccionar( 
    self,
    forma = None,
    nivel = 0,
    herencia = {},
    referente = None,
  ):
    nivel += 1
    """ Limpiar parametros q no se heredan.  """
    herencia.pop( 'forma', None )
    herencia.pop( 'reiterar', None )

    for unidad in forma:  
      try:
        #revisar
        if unidad not in self.paleta:
          error = "PISTA: \"" + self.nombre + "\""
          error += " NO ENCUENTRO: \"" + unidad + "\"  "  
          raise Excepcion( unidad, error )
          pass
        original = self.paleta[ unidad ]
        sucesion = {
          **original,
          **herencia,
        } 
        reiterar = 1
        if 'reiterar' in original:
          reiterar = original[ 'reiterar' ]
        for r in range( reiterar ):
          if 'forma' not in original: 
            segmento = Segmento(
              pista       = self,
              nombre      = unidad,
              nivel       = nivel - 1,
              orden       = len( self.segmentos ),
              recurrencia = sum( 
                [ 1 for e in self.segmentos if e.nombre == unidad ]
              ),
              propiedades = {
                **Segmento.defactos,
                **sucesion,
              }
            )
            if referente: 
              # registrar  q numero de recurrencia/id o de cual es clonnn
              segmento.referente = referente.nombre
            self.segmentos.append( segmento )
          else:
            seccion = Seccion(
              pista       = self.nombre,
              nombre      = unidad,
              nivel       = nivel - 1,
              orden       = len( self.secciones ),
              recurrencia = sum( 
                [ 1 for e in self.secciones if e.nombre == unidad ]
              ),
            )
            # registrar  q numero de recurrencia/id o de cual es clonnn
            seccion.referidos = original['forma'] 
            self.secciones.append( seccion )
            elemento = seccion
            self.seccionar( 
              original[ 'forma' ],
              nivel,
              sucesion,
              seccion,
            ) 
      except Excepcion as e:
          print( e )
