from argumentos import args, verboseprint, Excepcion

#import random
#import sys

class Segmento:
  """
  Secuencia > Segmentos > Articulaciones
  """
  cantidad = 0 
 
  def __str__( self ):
    o = '' 
    for attr, value in self.__dict__.items():
      l = str( attr ) + ':' + str( value )
      o += l + '\n'
    return o

  def __init__( 
    self,
    nombre,
    canal,
    reiterar,
    revertir,
    desplazar,
    referente,
    clave,
    metro,
    afinacionNota,
    afinacionBanco,
    afinacionPrograma,
    sysEx,
    uniSysEx,
    NRPN,
    RPN,
  ):
    self.orden = Segmento.cantidad 
    Segmento.cantidad += 1

    self.nombre     = nombre
    self.canal = canal
    self.reiterar = reiterar
    self.revertir = revertir
    self.desplazar = desplazar
    self.referente = referente
    self.clave = clave
    self.metro = metro
    self.afinacionNota = afinacionNota
    self.afinacionBanco = afinacionBanco
    self.afinacionPrograma = afinacionPrograma
    self.sysEx = sysEx
    self.uniSysEx = uniSysEx
    self.NRPN = NRPN
    self.RPN = RPN

    #self.articulaciones = [] 
    #print( self.articulaciones )

