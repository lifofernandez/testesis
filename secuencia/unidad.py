class Unidad():
  """
  Meta clase base para Secciones, Segmentos 
  """
  cantidad = 0 
  def __str__( self ):
    o  = str( self.numero ) + ' ' 
    if(self.numero < 10 ):
      o += ' ' 
    o += str( self.orden ) + ' ' 
    if(self.orden < 10 ):
      o += ' ' 
    o += str( self.nivel )  + '  '
    if(self.nivel < 10 ):
      o += ' ' 
    o += str( self.recurrencia ) + ' ' 
    if(self.recurrencia < 10 ):
      o += ' ' 
    o += '  ' 
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

