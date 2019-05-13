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
    self.dinamica  = int( dinamica * 126 )
    self.controles = controles
    self.altura    = nota
    self.tono      = tono
    self.acorde    = acorde

