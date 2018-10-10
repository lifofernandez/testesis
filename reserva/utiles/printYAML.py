#!/usr/bin/env python3

import argparse
import yaml
import weakref
import pprint

"""
Manejo de argumentos y parametros globales
"""
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
#parser.add_argument( 
# '-f',
# '--formato',
# help = 'Formato de salida (op: midi, musicxml, text).',
#)
args = parser.parse_args()
# Archivos de entrada
pistas = []
for archivo in args.archivos:
  data = open( archivo.name, 'r' )
  pistas.append( yaml.load( data ) )
# Verbosidat
verboseprint = print if args.verbosity else lambda *a, **k: None


for pista in pistas:
  pprint.pprint( pista )

