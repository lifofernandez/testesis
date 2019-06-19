from argumentos import args, verboseprint, Excepcion
import pprint
from segmento import Segmento
from seccion import Seccion
import random
import sys

class Pista:
  """
  Clase para cada definicion de a partir de archivos .yml
  PISTA > Secuencia > Secciones > Segmentos > Articulaciones
  """
  cantidad = 0 
  defactos = {
    # TO DO 
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
    o = '' 
    for attr, value in self.__dict__.items():
      l = str( attr ) + ':' + str( value )
      o += l + '\n'
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
    Pista.defacto = Segmento(
      pista = 'defacto',
      orden = 0,
      propiedades = {
        'nombre' : 'defacto',
        **Pista.defactos
      }
    )

    self.paleta     = paleta

    self.secuencia  = [] 
    #self.secuenciar( forma )


    self.SECCIONES = []

    self.seccionar( forma )
    print('SECCIONES')
    pprint.pprint( self.SECCIONES )
    
    verboseprint( '\n#### ' + self.nombre + ' ####' )

  """ Organiza unidades según relacion de referencia """
  cuenta = 0
  def seccionar( 
    self,
    forma = None,
    nivel = 0,
    seccion = None,
  ):
    nivel += 1

    destino = self.SECCIONES
    for unidad in forma:  
      original = self.paleta[ unidad ]
      self.cuenta +=1
      e = {
        'orden'  : self.cuenta,
        'nombre' : unidad,
        'nivel'  : nivel,
        #'suena'  : False,
        'recurrencia' : sum( 
          [ 1 for e in destino if e[ 'nombre' ] == unidad ]
        )
      }
      if seccion: 
        e['referente'] = seccion['nombre']
      destino.append(e)
      if 'forma' in original:
        # esto es una seccion 
        # e['cantidad_elementos'] = len( original['forma'] )
        e['referidos'] = original['forma'] 
        self.seccionar( 
          original[ 'forma' ],
          nivel,
          e,
        ) 

      #if seccion:
      #   seccion.setdefault( 'elementos' , [] )
      #   destino = seccion['elementos']
      ##  e['seccion'] = seccion['nombre']



      #if 'forma' not in original:
      #  # esto es un segmento
      #  e['suena'] = True
      #  #destino.setdefault( 'elementos' , [] ).append( e )
      #  destino.append( e )
      #  #print(unidad,destino)




      #if not rama:
      #  destino = self.SECCIONES
      #  destino.append( rama )
      #  #destino.setdefault( 'elementos' , [] ).append( rama )

      #if not padre:
      #  destino.append( h )
      #if padre:
      #  for s in destino:
      #    if s['nombre'] == padre['nombre']:
      #       if s['eo'] == False:
      #         #s.setdefault( 'hijos' , [] ).append( h )
      #         s['eo'] = True


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
#        reiterar = 1
#
#        if 'reiterar' in original:
#          reiterar = original[ 'reiterar' ]
#          
#        """ Crea parametros de unidad combinando originales con herencia """
#        sucesion = {
#          **original,
#          **herencia,
#          'nombre'      : unidad,
#          'recurrencia' : recurrencia,
#          'nivel'       : nivel,
#        } 
#
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
#            #  [ 1 for s in self.secciones if s[ 'nombre' ] == unidad ]
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

