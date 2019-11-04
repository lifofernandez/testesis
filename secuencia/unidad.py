class Unidad():
  """
  Meta clase base para Secciones, Segmentos 
  """
  cantidad = 0 
  def __str__( self ):
    o  = str( self.numero ) + '\t' 
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
    recurrencia,
    referente,
  ):
    self.pista  = pista 
    self.nombre = nombre
    self.nivel = nivel
    self.orden = orden
    self.recurrencia = recurrencia
    self.referente = referente
    self.numero = Unidad.cantidad 
    Unidad.cantidad += 1

