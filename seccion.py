from argumentos import args, verboseprint, Excepcion

class Seccion:
  """
  Pista > Secuencia > SECCION > Segmentos >  Articulaciones 
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
    id,
    pista,
    orden,
    #elementos,
  ):
    self.numero = Seccion.cantidad 
    Seccion.cantidad += 1

    self.id        = id 
    self.orden     = orden

    self.elementos = [] 

