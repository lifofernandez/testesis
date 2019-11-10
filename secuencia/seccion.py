from .unidad import Unidad

class Seccion(  Unidad ):

  """ Conjuntos de Secciones y/o Segmentos.
  Conserva relaciones de referencia a nivel lógico  
  """
  cantidad = 0

  def verbose( self, vebosidad = 0 ):
    #o =  ('=' * 70 ) + '\n'
    o = self.tipo + ''
    o += str( self.numero_seccion ) + ' ' 
    if(self.numero_seccion < 10 ):
      o += ' ' 
    o += str( self ) + ' '
    o += '=' * ( 8 - ( len( self.nombre ) + self.nivel ) )
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
    Unidad.__init__( 
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
