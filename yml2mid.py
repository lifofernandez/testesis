#!/usr/bin/env python3.7
import yaml
from dataclasses import dataclass

data = open("track.yml", 'r')
track = yaml.load( data )

@dataclass
class Track:
  parametros: dict
  estructura: dict
  articulacion: dict

  #@property
  #def altura( self ):
  #  return self.parametros['altura']

  @property
  # alturas son el resultado de combinar el parametro "altura"
  def alturas( self ):
    trasponer = self.parametros['altura']['octava'] * 12
    return evaluar( self.parametros['altura']['set'] ) 


  def __str__( self ):
    output = '' 
    for x in self.parametros:
      output += str(x) + '\n'  
      for y in self.parametros[x]:
        output += '  ' + str( y )+' : '+ str( self.parametros[x][y] ) + '\n'  
    return output 

  def secuenciar( self ):
    output = [] 
    for elem in self.articulacion:
      if type( elem ) is int or float:
        output.append( elem )
      elif type( elem ) is str:
          estructura = self['estructuras'][ elem ] 
          output.append( self.secuenciar( estructura ) )
      elif type(elem ) is list: 
          output = [ self.secuenciar( elem ) for e in i ]
    return output 

  @property
  def secuencia( self ):
    return self.secuenciar() 

def evaluar(i):
  if type( i ) is str:
    o = eval( i )
  elif type( i ) is list: 
    o = [ evaluar( e ) for e in i ]
  else:
    return False
  return o

melodia = Track( 
  track['parametros'],
  track['estructuras'],
  track['articulacion'],
)

print(melodia )
print(melodia.alturas[6][-1])
print(melodia.secuencia)


# TODO
# [ ] func/@property: Secuenciar estructuras.
#     Confeccionar lista de punteros a partir de estructuras contendoras de punteros.
# [ ] Que las escructuras levanten params por defencto .
# [ ] Que cada estructura pueda sobreescribir sus parametros.
# [ ] Agregar herencia entre estructuras.
