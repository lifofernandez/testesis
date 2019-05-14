from argumentos import args, verboseprint, Excepcion

class Articulacion:
  """
  Pista > Secuencia > Segmentos > ARTICULACIONES
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
    nombre,
    paso,
    bpm,
    programa,
    duracion,
    dinamica,
    nota,
    acorde,
    tono,
    controles,
  ):
    self.orden = Articulacion.cantidad 
    Articulacion.cantidad += 1

    self.nombre    = nombre
    self.posicion  = paso
    self.bpm       = bpm
    self.programa  = programa
    self.duracion  = duracion
    self._dinamica  = dinamica 
    self.controles = controles
    self.altura    = nota
    self.tono      = tono
    self.acorde    = acorde

  @property
  def dinamica(
    self
  ):
    viejo_valor = self._dinamica 
    viejo_min = 0 
    viejo_max = 1 
    nuevo_min = 0
    nuevo_max = 126 
    nuevo_valor = ( ( viejo_valor - viejo_min ) / ( viejo_max - viejo_min ) ) * ( nuevo_max - nuevo_min) + nuevo_min
    return int( min( max( nuevo_valor, nuevo_min ), nuevo_max ) )
