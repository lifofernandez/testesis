from argumentos import args, verboseprint, Excepcion

#import random
#import sys

class Segmento:
  """
  Secuencia > Segmentos > Articulaciones
  """
  cantidad = 0 
 
  def __str__( self ):
    o = '' 
    for attr, value in self.__dict__.items():
      l = str( attr ) + ':' + str( value )
      o += l + '\n'
    return o

  def __init__( 
    self,
    nombre,
  ):
    self.nombre     = nombre
    self.orden      = Segmento.cantidad 
    Segmento.cantidad += 1
    #self.articulaciones = [] 
    #print( self.articulaciones )

