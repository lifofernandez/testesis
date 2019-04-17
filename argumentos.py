"""
Argumentos y parametros globales
"""
import pprint
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
 '--verbosity',
 help = 'Imprimir informacion',
)
parser.add_argument( 
 '-o',
 '--output',
 default = 'output',
 help = 'Nombre del archivo de salida',
)
parser.add_argument( 
 '-p',
 '--plotear',
 help = 'Ploteo del arbol de relaciones entre unidades (dot ó png)',
)
args = parser.parse_args()

verboseprint = pprint.pprint if args.verbosity else lambda *a, **k: None

def error(
      e = '',
      info = ''
    ):    
    msg = "[ ERROR ] " + info + " "
    print( msg  + "=" * ( 80 - int( len( msg ) ) ) ) 
    print( e )
    print( "=" * 80 )
