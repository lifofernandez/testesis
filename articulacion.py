# TODO subcribir a Elemento()
from argumentos import args, verbose, Excepcion

class Articulacion:
  """
  Pista > Segmentos > ARTICULACIONES
  """
  cantidad = 0 
 
  def __str__( self ):
    o  = str( self.numero ) + '\t' 
    o += str( self.orden ) + '\t' 
    o += str( self.bpm)  + '\t'
    o += str( self.duracion) + '\t' 
    o += str( self.dinamica) + '\t' 
    o += str( self.altura) + '\t' 
    o += str( self.tono) + '\t' 
    o += str( self.controles) + '\n' 
    return o  

  def __init__( 
    self,
    segmento, 
    orden,
    bpm,
    programa,
    duracion,
    dinamica,
    nota,
    acorde,
    tono,
    controles,
  ):
    self.numero = Articulacion.cantidad 
    Articulacion.cantidad += 1

    self.segmento  = segmento
    self.orden     = orden
    self.bpm       = bpm
    self.programa  = programa
    self.tono      = tono
    self._dinamica  = dinamica 
    self.duracion  = duracion
    self.controles = controles
    self.altura    = nota
    self.acorde    = acorde

  @property
  def precedente( self ):
    n = self.orden
    o = self.segmento.articulaciones[ n - 1]
    if  n == 0:
      o = self.segmento.precedente.articulaciones[ - 1 ]
    return o 

  def obtener( self, key ):
      try:
        o = getattr( self, key )
        return o
      except AttributeError as e:
        return e

  def cambia( self, key ):
      if self.segmento.orden == 0 and self.orden == 0:
        return True
      anterior = self.precedente.obtener( key )
      este = self.obtener( key ) 
      return anterior != este

  @property
  def dinamica(
    self
  ):
    viejo_valor = self._dinamica 
    viejo_min = 0 
    viejo_max = 1 
    nuevo_min = 0
    nuevo_max = 126 
    nuevo_valor = (
      ( viejo_valor - viejo_min ) / ( viejo_max - viejo_min )
    ) * ( nuevo_max - nuevo_min) + nuevo_min
    return int( min( max( nuevo_valor, nuevo_min ), nuevo_max ) )

