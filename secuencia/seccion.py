from .elemento import Elemento

class Seccion( Elemento ):
  cantidad = 0
  """ Pista > SECCION > Segmentos > Articulaciones """

  def verbose( self, vebosidad = 0 ):
    #o =  ('=' * 70 ) + '\n'
    o = self.tipo + ''
    o += str( self.numero_seccion ) + '\t' 
    o += str( self ) + ' '
    o += '=' * ( 28 - ( len( self.nombre ) + self.nivel ) )
    return o

  def __init__( 
    self,
    pista, 
    nombre,
    nivel,
    orden,
    recurrencia,
    referente
  ):
    Elemento.__init__( 
      self,
      pista, 
      nombre,
      nivel,
      orden,
      recurrencia,
      referente
    )
    self.numero_seccion = Seccion.cantidad 
    Seccion.cantidad += 1
    self.nivel = nivel
    self.tipo = 'SECC'
