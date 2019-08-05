import importlib.util as importar

class Complemento:

    """ Interfaz minimalista para complementos de usuario

        metodo: 
           metodo:
           # propiedad_a_modificar1: valor
           # propiedad_a_modificar2: valor
         # metodo2:
           # argumento1: valor
           # argumento2: valor
      """
    cantidad = 0
    registro = []
    def __init__(
      self,
      path
    ):
     self.path = path
     self.nombre = path.split('.')[0]
     Complemento.cantidad += 1
     spec = importar.spec_from_file_location(
       self.nombre,
       self.path
     )
     if spec: 
       modulo = importar.module_from_spec( spec )
       spec.loader.exec_module( modulo )
       self.modulo = modulo

    def __str__(
      self,
    ):
      return self.nombre
