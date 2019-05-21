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
    self.tono      = tono

    self._dinamica  = dinamica 
    self.duracion  = duracion
    self.controles = controles
    self.altura    = nota
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

  #def next(self):
  #        try:
  #            result = self.collection[self.index]
  #            self.index += 1
  #        except IndexError:
  #            raise StopIteration
  #        return result
  #
  #def previo(self):
  #    self.index -= 1
  #    if self.index < 0:
  #        raise StopIteration
  #    return self.collection[self.index]

