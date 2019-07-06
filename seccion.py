#from argumentos import args, verboseprint, Excepcion
from elemento import Elemento

class Seccion( Elemento ):
  cantidad = 0
  """ Pista > SECCION > Segmentos > Articulaciones """
  #def __str__( self ):
  #  o = Elemento.__str__( self )
  #  o += self.tipo + ' '
  #  o += str( self.numero_seccion ) 
  #  return o  

  def verbose( self, verbose = 0 ):
    o = self.tipo + ' '
    o += str( self.numero_seccion ) + '\t' 
    o += str( self ) + ' '
    #o += '=' * ( 60 - len( o ))
    o += '=' * ( 18 - (len( self.nombre ) + self.nivel ))
    return o

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
    self.numero_seccion = Seccion.cantidad 
    Seccion.cantidad += 1
    self.nivel = nivel
    self.tipo = 'SECC'
