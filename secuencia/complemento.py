import importlib.util as importar

class Complemento:

    """ Interfaz para complementos de usuario.

        Declarar ubicación del paquete en propiedades de track.
        complementos: 'enchufes.py'

        En propiedades de segmento invocar metodo y subscribir, propiedad y
        argumentos.

        metodo: # en: enchufes.py
          propiedad_a_manipular1: argumentos
          propiedad_a_manipular2: argumentos
        fluctuar:
          dinamicas: .5 
          alturas: 2 
    """

    cantidad = 0
    registro = []

    def __str__(
      ubicacion,
    ):
      return self.nombre

    def __init__(
      self,
      ubicacion
    ):
     self.ubicacion = ubicacion
     self.nombre = ubicacion.split( '.' )[ 0 ]
     Complemento.cantidad += 1
     spec = importar.spec_from_file_location(
       self.nombre,
       self.ubicacion
     )
     if spec: 
       modulo = importar.module_from_spec( spec )
       spec.loader.exec_module( modulo )
       self.modulo = modulo

