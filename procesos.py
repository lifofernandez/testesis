
#paquete: 
  # metodo:
    # propiedad_a_modificar1: valor
    # propiedad_a_modificar2: valor
  # metodo2:
    # argumento1: valor
    # argumento2: valor

def fluctuar( entrada = 'eo' ):
  salida = entrada + 'oa'
  return salida

#@property
#def fluctuar( self ):
#  # fluctuar a cualquier parametro de la articulacion
#  fluctuar = self.props['fluctuar']
#  rand_min = 0
#  if 'min' in fluctuar:
#    rand_min = fluctuar['min'] 
#  rand_max = 0
#  if 'max' in fluctuar:
#    rand_max = fluctuar['max']
#  f = random.uniform( 
#    rand_min,
#    rand_max 
#  ) if rand_min or rand_max else 1
#  return f 
