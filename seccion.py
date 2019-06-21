#from argumentos import args, verboseprint, Excepcion
from elemento import Elemento

class Seccion( Elemento ):
  cantidad = 0
  """
  Pista > Secuencia > SECCION > Segmentos > Articulaciones 
  """
  def __init__( 
    self,
    pista, 
    nombre,
    nivel,
    orden,
    recurrencia,
  ):
    Elemento.__init__( 
      self,
      pista, 
      nombre,
      nivel,
      orden,
      recurrencia
    )
    self.numero = Seccion.cantidad 
    Seccion.cantidad += 1
    self.tipo = 'SECCION'
