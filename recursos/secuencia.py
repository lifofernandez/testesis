from argumentos import args, verboseprint, Excepcion

class Secuencia:
  """
  Pista > SECUENCIA > Segmentos > Articulaciones
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
    entrada
  ):
    self.orden = Secuencia.cantidad 
    Secuencia.cantidad += 1
    self = entrada
    #https://stackoverflow.com/questions/49682296/how-to-elegantly-pass-all-attributes-of-a-class-as-arguments-in-a-function
