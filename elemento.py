#from argumentos import args, verboseprint, Excepcion
#import pprint

class Elemento():
  """
  Pista > ELEMENTOS
  Clase base para, Secciones, Segmentos y Articulaciones
  """
  cantidad = 0 
  # TODO, agregar func/prop registre mayor de recurrencia nivel

  def __str__( self ):
    o  = str( self.numero ) + '\t' 
    # TODO numero de elemento, orden en la pista y orden en la SECCION
    o += str( self.orden ) + '\t' 
    o += str( self.nivel )  + '\t'
    o += str( self.recurrencia ) + '\t' 
    o += '+' + str( '-' * ( self.nivel ) ) 
    o += self.nombre  
    return o  

  def __init__( 
    self,
    pista, 
    nombre,
    nivel,
    orden,
    recurrencia
  ):
    self.pista  = pista 
    self.nombre = nombre
    self.nivel = nivel
    self.orden = orden
    self.recurrencia = recurrencia
    self.numero = Elemento.cantidad 
    Elemento.cantidad += 1

