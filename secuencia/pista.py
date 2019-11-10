import os
from argumentos import Excepcion
from .complemento import Complemento
from .seccion  import Seccion
from .segmento import Segmento

class Pista:
  """
  Clase para cada definicion de a partir de archivos .yml
  Secuencia > PISTA > Secciones > Segmentos > Articulaciones
  """
  cantidad = 0 

  defactos = {
    'nombre'       : '',
    'unidades'     : [ None ],
    'forma'        : [ None ],
    'complementos' : None,
  }

  def __str__( self ):
    o  = 'PISTA ' + str( self.numero) + ': '+ str( self.nombre  )
    return o

  def verbose( self, verbosidad = 0 ):
    if verbosidad > 0:
      o = str( self ) + ' '
      o = str( self ) + ' '
      if verbosidad > 1:
        o += '\n       id #  LVL RCR\n'
        :q
        :q
        for e in self.elementos:
          o += e.verbose( verbosidad ) 
          o += '\n'
      return o

  def __init__( 
    self,
    nombre,
    paleta,
    forma,
    plugin,
    secuencia,
  ):
    self.nombre     = nombre
    self.paleta     = paleta
    self.forma      = forma 
    self.secuencia  = secuencia
    self.plugin     = plugin
    self.numero     = Pista.cantidad 
    Pista.cantidad += 1

    self.secciones  = []
    self.segmentos  = []
    self.seccionar( self.forma )

  @property
  def complemento( self ):
    ruta = self.plugin
    c = None 
    if ruta and os.path.exists( ruta ):
      # TODO Tirar excepción
      # and p not in Complemento.registro:
      Complemento.registro.append( ruta )
      c = Complemento( ruta )
    return c

  @property
  def elementos( self ):
    return sorted( 
      self.secciones + self.segmentos,
      key = lambda x: x.numero
    )

  @property
  def tiempo( self ):
    # duracion en segundos
    return sum( [ s.tiempo for s in self.segmentos ] ) 

  """ Organiza unidades según relacion de referencia """
  def seccionar( 
    self,
    forma = None,
    nivel = 0,
    herencia = {},
    referente = None,
  ):
    nivel += 1
    """ Limpiar parametros q no se heredan.  """
    herencia.pop( 'forma', None )
    herencia.pop( 'reiterar', None )

    for unidad in forma:  
      try:
        if unidad not in self.paleta:
          error = "PISTA: \"" + self.nombre + "\""
          error += " NO ENCUENTRO: \"" + unidad + "\"  "  
          raise Excepcion( unidad, error )
          pass
        original = self.paleta[ unidad ]
        sucesion = {
          **original,
          **herencia,
        } 
        reiterar = 1
        if 'reiterar' in original:
          reiterar = original[ 'reiterar' ]
        for r in range( reiterar ):
          if 'forma' not in original: 
            segmento = Segmento(
              pista       = self,
              nombre      = unidad,
              nivel       = nivel - 1,
              orden       = len( self.segmentos ),
              recurrencia = sum( 
                [ 1 for e in self.segmentos if e.nombre == unidad ]
              ),
              referente = referente,
              propiedades = sucesion,
            )
            self.segmentos.append( segmento )
          else:
            seccion = Seccion(
              pista       = self.nombre,
              nombre      = unidad,
              nivel       = nivel - 1,
              orden       = len( self.secciones ),
              recurrencia = sum( 
                [ 1 for e in self.secciones if e.nombre == unidad ]
              ),
              referente   = referente,
            )
            seccion.referidos = original['forma'] 
            self.secciones.append( seccion )
            elemento = seccion
            self.seccionar( 
              original[ 'forma' ],
              nivel,
              sucesion,
              seccion,
            ) 
      except Excepcion as e:
          print( e )
