#!/usr/bin/env python3.7

import yaml
from dataclasses import dataclass

data = open( "track.yml", 'r' )
track = yaml.load( data )

@dataclass
class Track:
  parametros: dict
  estructuras: dict
  articulacion: dict

  #@property
  #def altura( self ):
  #  return self.parametros['altura']

  def __str__( self ):
    output = '' 
    for x in self.parametros:
      output += str(x) + '\n'  
      for y in self.parametros[x]:
        name = '  ' + str( y )
        valu = ': ' + str( self.parametros[x][y] ) 
        output += name + valu + '\n'  
    return output 

  @property
  # alturas son el resultado de combinar el propiedades adentro del parametro "altura"
  def alturas( self ):
    #octavar = self.parametros['altura']['octava'] * 12
    #trasponer = octavar + self.parametros['altura']['trasponer'] 
    evaluado =  evaluar( self.parametros['altura']['set'] ) 
    return evaluado 


  #@property
  #def secuenciar( inp ):
  #  output = [] 
  #  for item in inp:
  #    if type( item ) is int or float:
  #      puntero = item 
  #      output.append( puntero )
  #    elif type( item ) is str:
  #        estructura = self['estructuras'][ item ] 
  #        self.secuenciar( estructura )
  #    elif type( item ) is list: 
  #      for e in item :
  #        estructuras = self['estructuras'][ e ] 
  #        self.secuenciar( e )
  #        # e = [ self.secuenciar( elem ) for e in i ]
  #  return output 

  @property
  def secuencia( self ):
      return secuenciar( self.articulacion, self.estructuras )



def secuenciar( articulacion, estructuras ):
  """
  numero = puntero, string = estructura o rutina
  ¿if string && is not 'otra estructura' then eval?
  ¿if string 'otra estructura' then read?
  ¿eval resultado == numeros return punteros?
  ¿como saber si es micro? minusculas? 
  ¿importa si son micro? 
  ¿si es lista de numero es micro, o no?
  ¿si son numeros son micro?
  micro:
  Args: lista de estructuras a aplanar, paleta de estructuras
  """
  output = [] 
  for item in articulacion:
    if ( isinstance( item, int ) ):
      puntero = item 
      output.append( puntero )
    elif ( isinstance( item, list) ):
      #for element in item:
      estructura = item
      output += secuenciar( estructura , estructuras ) 
    elif isinstance( item, str ) :
       if item in estructuras:
         estructura = estructuras[ item ] 
         output += secuenciar( estructura , estructuras ) 
       else:
         evaluado = evaluar( item ) 
         output += secuenciar( evaluado , estructuras ) 
  return output 

def evaluar(i):
  if type( i ) is int :
      return i
  if type( i ) is float:
      return i
  if type( i ) is str:
    o = eval( i )
  elif type( i ) is list: 
    o = [ evaluar( e ) for e in i ]
  else:
    return False
  return o

'https://stackoverflow.com/questions/2357230'
aplanar = lambda l: [item for sublist in l for item in sublist]

melodia = Track( 
  track['parametros'],
  track['estructuras'],
  track['articulacion'],
)

print(melodia)
# en realidad melida.motivo['a'].alturas
print(melodia.alturas)
# melodia.secuencia
# ¿sería melida.motivo['a'].secuencia ?

print(melodia.secuencia)

pepe = [[1,[888],2,3],[4,5,6], [7], [8,9]] * 9
print( aplanar(pepe) )


""" TODO
[-] func/@property: Secuenciar estructuras.
[ ] Punteros a partir de estructuras contendoras de punteros.
[ ] Que las escructuras levanten params por defencto .
[ ] Que cada estructura pueda sobreescribir sus parametros.
[ ] Agregar herencia entre estructuras.
[ ] proper eval() https://docs.python.org/3/library/ast.html 
"""

