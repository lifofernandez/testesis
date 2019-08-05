#import math
import random
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

def desplazar(
    entrada = 1,
    parametro = 1
  ):
  return [ a + parametro for a in entrada ]

def fluctuar( entrada = [ 1 ], factor = .5 ):
  salida = []
  for a in entrada:
    rand_min = a - (factor / 2)
    rand_max = a + (factor / 2)
    f = random.uniform( 
      rand_min,
      rand_max 
    ) 
    salida.append( f )
  return salida

