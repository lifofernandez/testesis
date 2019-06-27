from argumentos import args, verboseprint, Excepcion
import pprint
from elemento import Elemento
from seccion  import Seccion
from segmento import Segmento

#from elemento import Elemento, Seccion, Segmento

import random
import sys

class Pista:
  """
  Clase para cada definicion de a partir de archivos .yml
  PISTA > Secuencia > Secciones > Segmentos > Articulaciones
  """
  cantidad = 0 
  defactos = {
    # TO DO Meta Track
    # Agrupar/Revisar/Avisar propiedades "Globales" 
    # que NO refieren a un canal en particualr
    #'addTrackName',
    #'addCopyright',

    #'addTempo',
    #'addTimeSignature',
    #'addKeySignature',
    #'changeNoteTuning',
    #'addSysEx',
    #'addUniversalSysEx',

    # Propiedades de Segmento 
    'canal'             : 1,
    'desplazar'         : 0,
    'metro'             : '4/4',
    'clave'             : { 'alteraciones' : 0, 'modo' : 0 },
    'fluctuacion'       : { 'min' : 1, 'max' : 1 },
    'transportar'       : 0,
    'transponer'        : 0,
    'reiterar'          : 1,
    'referente'         : None,
    'revertir'          : None,
    'afinacionNota'     : None,
    'afinacionBanco'    : None,
    'afinacionPrograma' : None,
    'sysEx'             : None,
    'uniSysEx'          : None,
    'NRPN'              : None,
    'RPN'               : None,

    # Propiedades de Articulacion 
    'BPMs'         : [ 60 ],
    'programas'    : [ 1 ],
    'duraciones'   : [ 1 ],
    'dinamicas'    : [ 1 ],
    'registracion'   : [ 1 ],
    'alturas'      : [ 1 ],
    'tonos'        : [ 0 ],
    'voces'        : None,
    'controles'    : None,
  }

  def __str__( self ):
    # Esto es para verbose print level 1
    o = 'PISTA ' + str( self.numero) + ': '+ str( self.nombre)

    # Esto es para verbose print level 2
    o +=  '\nid\torden\tnivel\trecur\tnombre\n'
    for s in self.secciones:
      o += str(s) + '\n'
    return o

  def __init__( 
    self,
    nombre,
    paleta,
    forma
  ):
    self.nombre     = nombre
    self.numero     = Pista.cantidad 
    Pista.cantidad += 1
    self.paleta = paleta
    self.forma = forma 

    # hacer uno para todas las pistas
    # sacar de la cuenta general
    Pista.defacto = Segmento(
      pista = nombre,
      nombre = 'Segmento Defacto:' + nombre,
      nivel = None,
      orden = None,
      recurrencia = None,
      propiedades = {
        **Pista.defactos
      }
    )


    self.secuencia  = [] 
    #self.secuenciar( forma )

    #self.secciones = self.seccionar( self.forma )
    self.secciones = []
    self.seccionar( self.forma )

    # esto no va aca
    verboseprint( self )

  @property
  def segmentos( 
    self
  ):
    segmentos = []
    for s in self.secciones:
        if s.__class__.__name__ == 'Segmento':
          segmentos.append(s)
    return segmentos
  

  """ Organiza unidades según relacion de referencia """
  def seccionar( 
    self,
    forma = None,
    nivel = 0,
    herencia = {},
    referente = None,
  ):
    nivel += 1
    """ Limpiar parametros q no se heredan.  """
    herencia.pop( 'forma', None )
    herencia.pop( 'reiterar', None )
    for unidad in forma:  
      try:
        if unidad not in self.paleta:
          error = "PISTA: \"" + self.nombre + "\""
          error += " NO ENCUENTRO: \"" + unidad + "\"  "  
          raise Excepcion( unidad, error )
          pass
        original = self.paleta[ unidad ]
        args = {
          'pista'      : self.nombre,
          'nombre'     : unidad,
          'nivel'      : nivel - 1,
          'orden'      : len( self.secciones ),
          'recurrencia': sum( 
            [ 1 for e in self.secciones if e.nombre == unidad ]
          )
        }
        sucesion = {
          **original,
          **herencia,
        } 
        if 'forma' not in original: 
          elemento = Segmento(
            **args, 
            propiedades = {
              **Pista.defactos,
              **sucesion,
            }
          )

        else:
          elemento = Seccion( **args )
          # registrar recurrencia/id
          elemento.referidos = original['forma'] 
        if referente: 
          # registrar recurrencia/id
          elemento.referente = referente.nombre

        reiterar = 1
        if 'reiterar' in original:
          reiterar = original[ 'reiterar' ]
        """ Cantidad de repeticiones de la unidad. """
        for r in range( reiterar ):
          self.secciones.append( elemento )
          if 'forma' in original:
            self.seccionar( 
              original[ 'forma' ],
              nivel,
              sucesion,
              elemento,
            ) 
      except Excepcion as e:
          print( e )



#  """ Organiza unidades según relacion de referencia """
#  def secuenciar( 
#    self,
#    forma    = None,
#    nivel    = 0,
#    herencia = {},
#    padre = None,
#    #secciones = []
#  ):
#    print(nivel)
#    nivel += 1
#    """ Limpiar parametros q no se heredan.  """
#    herencia.pop( 'forma', None )
#    herencia.pop( 'reiterar', None )
#    error = "PISTA \"" + self.nombre + "\""
#
#    """ Recorre lista d unidades principales.  """
#    cuenta_secciones = 0
#    cuenta_segmentos = 0
#    for unidad in forma:  
#      verboseprint( '-' * ( nivel - 1 ) +  unidad )
#      try:
#        if unidad not in self.paleta:
#          error += " NO ENCUENTRO \"" + unidad + "\"  "  
#          raise Excepcion( unidad, error )
#          pass
#        original = self.paleta[ unidad ]
#
#        """ Cuenta recurrencias de esta unidad en este nivel.  """
#        recurrencia = 0
#          
#        """ Crea parametros de unidad combinando originales con herencia """
#        sucesion = {
#          **original,
#          **herencia,
#        } 
#
#        reiterar = 1
#        if 'reiterar' in original:
#          reiterar = original[ 'reiterar' ]
#        """ Cantidad de repeticiones de la unidad. """
#        for r in range( reiterar ):
#          destino = self.secciones
#          h = {
#            'nombre' : unidad,
#            #'recurrencia' : 0,
#            'recurrencia' : sum( 
#              [ 1 for s in destino if s[ 'nombre' ] == unidad ]
#            ),
#            'pasada':1,
#            'nivel':nivel,
#            'eo': False
#          }
#          if 'forma' in original:
#            #h['hijos'] = original['forma'] 
#            destino = original['forma'] 
#            h['cantidad_hijos'] = len( original['forma'] )
#            for hije in original['forma']:
#              h = {
#                'nombre' : h,
#                #'recurrencia' : 0,
#                'recurrencia' : sum( 
#                  [ 1 for s in destino if s[ 'nombre' ] == hije]
#                ),
#                'pasada':1,
#                'nivel':nivel,
#                'eo': False
#              }
#               h.setdefault( 'hijos' , [] ).append( hije )
#             
#
#            """ Si esta tiene parametro "forma" es una seccio es una seccion
#            refiere a otras unidades "hijas"
#            crea una seccion y pasa de vuelta por esta metodo.  """
#            seccion_n = Seccion(
#              id = unidad,
#              pista = self.nombre,
#              orden = cuenta_secciones,
#            )
#            cuenta_secciones += 1
#
#            self.secuenciar( 
#              original[ 'forma' ],
#              nivel,
#              sucesion,
#              h,
#            ) 
#
#
#          if 'forma' not in original:
#            """ Si esta unidad NO refiere a otra unidad = "celula" """
#            segmento = Segmento(
#              pista       = self.nombre,
#              orden       = cuenta_segmentos,
#              propiedades = {
#                **Pista.defactos,
#                **sucesion,
#              }
#            )
#            cuenta_segmentos += 1
#            self.secuencia.append( segmento )
#            #self.secuencia.append( seccion )
#
#
#          if not padre:
#            #h['recurrencia'] = sum( 
#            #[ 1 for s in self.secciones if s[ 'nombre' ] == unidad ]
#            #) 
#            destino.append( h )
#
#          if padre:
#            for s in destino:
#              if s['nombre'] == padre['nombre']:
#                 if s['eo'] == False:
#                   #s.setdefault( 'hijos' , [] ).append( h )
#                   s['eo'] = True
#          #    #s.setdefault( 'PASADO' , )
#          #    #h.setdefault( 'hijos' , original['forma'])
#
#          #    #s['hijos'].append( h )
#
#      except Excepcion as e:
#          print( e )

