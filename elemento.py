#from argumentos import args, verboseprint, Excepcion
#import pprint

class Elemento:
  """
  Pista > ELEMENTOS
  Clase base para, Secciones, Segmentos y Articulaciones
  """
  cantidad = 0 
  def __str__( self ):
    # metodo para devel/debugg print (evitar o mejorar)
    o = '' 
    for attr, value in self.__dict__.items():
      l = str( attr ) + ':' + str( value )
      o += l + '\n'
    return o

  def __init__( 
    self,
    pista, 
    numero,
    nombre,
    nivel,
    recurrencia
  ):
    self.pista  = pista 
    self.numero = numero 
    self.nombre = nombre
    self.nivel = nivel
    self.recurrencia = recurrencia
    self.numero = Elemento.cantidad 
    Elemento.cantidad += 1

