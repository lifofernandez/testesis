#!/usr/bin/env python3.7
import yaml
from dataclasses import dataclass

data = open("track.yml", 'r')
track = yaml.load( data )

@dataclass
class Track:
  parametros: dict
  estructuras: dict
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
  output = [] 
  for item in articulacion:
    if ( isinstance( item, int ) ):
      puntero = item 
      output.append( puntero )
    elif ( isinstance( item, str ) ):
      estructura = estructuras[ item ] 
      output += secuenciar(estructura , estructuras ) 
    elif ( isinstance( item, list) ):
      #for element in item:
      estructura = item
      output += secuenciar(estructura , estructuras ) 
  return output 

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

#print(melodia )
#print(melodia.alturas[6][-1])
#melodia.secuencia
print(melodia.secuencia)


# TODO
# [ ] func/@property: Secuenciar estructuras.
#     Confeccionar lista de punteros a partir de estructuras contendoras de punteros.
# [ ] Que las escructuras levanten params por defencto .
# [ ] Que cada estructura pueda sobreescribir sus parametros.
# [ ] Agregar herencia entre estructuras.
