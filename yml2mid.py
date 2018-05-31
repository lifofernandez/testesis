#!/usr/bin/env python3.7
import yaml
from dataclasses import dataclass

data = open("track.yml", 'r')
track = yaml.load( data )

@dataclass
class Track:
  parametros: dict
  estructura: dict

  @property
  def intervalos( self ):
    return self.parametros['intervalos']

  @property
  def set( self ):
    return evaluar( self.intervalos['set'] ) 

  @property
  def trasponer( self ):
    return self.intervalos['trasponer'] 

  @property
  def octava( self ):
    return self.intervalos['octava'] * 12

  def __str__( self ):
    output = '' 
    for x in self.parametros:
      output += str(x) + '\n'  
      for y in self.parametros[x]:
        output += '  ' + str( y )+' : '+ str( self.parametros[x][y] ) + '\n'  
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
)

print(melodia )
print(melodia.set[6][-1])



#oa = yaml.dump( eo,  default_flow_style = False )
#with open("data.yml", 'r') as stream:
#    try:
#        print( yaml.load( stream ) )
#    except yaml.YAMLError as exc:
#        print(exc)
