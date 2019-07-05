""" Argumentos y parametros globales """
import pprint
import datetime
ahora = datetime.datetime.now()

import argparse
parser = argparse.ArgumentParser()

parser.add_argument( 
 'archivos',
 help  = 'Al menos un archivo en formato YAML para procesar',
 type  = argparse.FileType( 'r' ),
 nargs = '+'
)

parser.add_argument( 
 '-v',
 '--verbose',
 action  = 'count',
 default = 0,
 help    = 'Imprimir información',
)

parser.add_argument( 
 '-o',
 '--output',
 default = 'output',
 help = 'Nombre del archivo de salida',
)

parser.add_argument( 
 '-c',
 '--copyright',
 default = str( ahora.year ),
 help    = 'Información de autoría',
)

args = parser.parse_args()

#verbose = print if args.verbose else lambda *a, **k: None

def verbose( e ):
  if args.verbose:
    print( e )

#print( args.verbose )

class Excepcion( Exception ):
  """Excepción basica para Pifies invocados por """
  def __init__( self, o, msg = None ):
    if msg is None:
      msg = "Un error ocurrio con %s" % o
    msg += "\n" + "=" * 80
    super( 
      Excepcion,
      self
    ).__init__( "[ ERROR ] " + msg )
    self.o = o

