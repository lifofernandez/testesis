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

#class Pifie( Exception ):    
#    """ Error basico """
#    #self.info = info 
#    #msg = "[ ERROR ] " + self.info + " "
#    #print( msg  + "=" * ( 80 - int( len( msg ) ) ) ) 
#    print( "*" * 80 )
#    pprint.pprint( Exception )
#    print( "=" * 80 )

class Pifie( Exception ):
    """Excepción basica para errores invocados por Pifie"""
    def __init__( self, o, msg = None ):
        if msg is None:
            # Set some default useful error message
            msg = "Un error ocurrio con %s" % o
        #print( msg  + "=" * (80 - int( len( msg ) )) ) 
        #print( o )
        #print( "=" * 80 )
        super( 
          Pifie,
          self
        ).__init__( "[ ERROR ] " + msg )
        self.o = o

#class CarCrashError(CarError):
#    """When you drive too fast"""
#    def __init__(
#          self,
#          car,
#          other_car,
#          speed
#        ):
#        super(CarCrashError, self).__init__(
#            car, msg="Car crashed into %s at speed %d" % (other_car, speed))
#        self.speed = speed
#        self.other_car = other_car

#Then, any code can inspect the exception to take further action:

#try:
#    drive_car(car)
#except CarCrashError as e:
#    # If we crash at high speed, we call emergency
#    if e.speed >= 30:
#        call_911()

#class MylibError(Exception):
#    """Generic exception for mylib"""
#    def __init__(self, msg, original_exception):
#        super(MylibError, self).__init__(msg + (": %s" % original_exception))
#        self.original_exception = original_exception
#
#try:
#    requests.get("http://example.com")
#except requests.exceptions.ConnectionError as e:
#     raise MylibError("Unable to connect", e)
