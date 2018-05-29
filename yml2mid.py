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
    
    return evaluar(self.intervalos['set']) 

  @property
  def trasponer( self ):
    return self.intervalos['trasponer'] 

  @property
  def octava( self ):
    return self.intervalos['octava'] * 12


  def params( self ):
    for param in self.parametros:
      print( param )
      for item in self.parametros[param]:
        print( '  ' + item + ' : ' + item )


def evaluar(i):
  if type(i) is str:
    return eval (i)
  else:
    return i

pista1 = Track( 
  track['parametros'],
  track['estructura'],
)

pista1.params()
#print( pista1.parametros['intervalos'])
print( pista1.set[-1])
#print( pista1.estructura)



# oa = yaml.dump( eo,  default_flow_style = False )
#with open("data.yml", 'r') as stream:
#    try:
#        print( yaml.load( stream ) )
#    except yaml.YAMLError as exc:
#        print(exc)
