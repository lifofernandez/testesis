#from argumentos import args, verboseprint, Excepcion
#import pprint

class Elemento:
  """
  Pista > ELEMENTOS
  Clase base para, Secciones, Segmentos y Articulaciones
  """
  cantidad = 0 
  # TODO, agregar func/prop registre mayor de recurrencia nivel

  def __str__( self ):
    # Esto es para verbose level 2
    o = str(self.numero) + '\t' 
    o += str(self.nivel) + '\t'
    o += str(self.recurrencia) + '\t' 
    o += '+' + str( '-' * ( self.nivel ) ) 
    o += self.nombre + '\t'
    if self.tipo:
      o += self.tipo + '\t'
    return o  

    # metodo para devel/debugg print ( mejorar )
    #o = '' 
    #for attr, value in self.__dict__.items():
    #  l = str( attr ) + ':' + str( value )
    #  o += l + '\n'
    #return o

  def __init__( 
    self,
    pista, 
    nombre,
    nivel,
    recurrencia
  ):
    self.pista  = pista 
    self.nombre = nombre
    self.nivel = nivel
    self.recurrencia = recurrencia
    self.numero = Elemento.cantidad 
    Elemento.cantidad += 1
    self.tipo = None 

