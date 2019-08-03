"""
Modulo de Métodos de usuario

Para "conectar", en la definicion de track:
procesos: 
  metodo1:
    propiedad_a_modificar1: args
    propiedad_a_modificar2: args
  metodo2:
    propiedad_a_modificar1: args
    propiedad_a_modificar2: args
"""

def probar( entrada = 1):
  salida = entrada * 7
  return salida

def fluctuar( entrada = [1] ):
  salida = entrada + [2,3]
  #fluctuar = self.props['fluctuar']
  #rand_min = 0
  #if 'min' in fluctuar:
  #  rand_min = fluctuar['min'] 
  #rand_max = 0
  #if 'max' in fluctuar:
  #  rand_max = fluctuar['max']
  #f = random.uniform( 
  #  rand_min,
  #  rand_max 
  #) if rand_min or rand_max else 1
  #return f 
  return salida

