from argumentos import args, verboseprint, Excepcion
from articulacion import Articulacion

import random
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
    intervalos,
    transponer,
    transportar,
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
    programas,
    duraciones,
    BPMs,
    dinamicas,
    fluctuacion,
    alturas,
    tonos,
    voces,
    capas,
  ):
    self.orden = Segmento.cantidad 
    Segmento.cantidad += 1

    self.nombre            = nombre
    self.canal             = canal
    self.reiterar          = reiterar
    self.revertir          = revertir
    self.desplazar         = desplazar
    self.referente         = referente
    self.clave             = clave
    self.metro             = metro
    self.afinacionNota     = afinacionNota
    self.afinacionBanco    = afinacionBanco
    self.afinacionPrograma = afinacionPrograma
    self.sysEx             = sysEx
    self.uniSysEx          = uniSysEx
    self.NRPN              = NRPN
    self.RPN               = RPN

    # internos
    #programas
    #intervalos
    #duraciones
    #BPMs     
    #dinamicas
    #alturas 
    #tonos  
    #voces 
    #capas

    ganador_voces = [ 0 ]
    if voces:
      ganador_voces = max( voces, key = len) 
    ganador_capas = [ 0 ]
    if capas:
      ganador_capas = max( capas , key = len) 

    """
    Evaluar que parametro lista es el que mas valores tiene.
    """
    candidatos = [ 
      dinamicas,
      duraciones,
      alturas,
      ganador_voces,
      ganador_capas,
      tonos,
      BPMs,
      programas,
    ]
    ganador = max( candidatos, key = len )
    pasos = len( ganador )

    """
    Consolidad "articulacion" 
    combinar parametros: altura, duracion, dinamica, etc.
    """
    ARTICULACIONES = []
    for paso in range( pasos ):
      bpm = BPMs[ paso % len( BPMs ) ]
      programa = programas[ paso % len( programas ) ]
      programa = 1
      duracion = duraciones[ paso % len( duraciones ) ]

      """
      Variaciones de dinámica.
      TODO: PASAR A ARTICULACION
      """
      #if 'min' in fluctuacion: rand_min = fluctuacion['min'] 
      #if 'max' in fluctuacion: rand_max = fluctuacion['max']
      #fluctuacion = random.uniform( 
      #   rand_min,
      #   rand_max 
      #) if rand_min or rand_max else 1
      fluctuacion = 1
      """
      Asignar dinámica.
      """
      dinamica = dinamicas[ paso % len( dinamicas ) ] * fluctuacion
      """
      Alturas, voz y superposición voces.
      """
      altura = alturas[ paso % len( alturas ) ]
      tono   = tonos[ paso % len( tonos ) ]
      acorde = []
      nota   = 'S' # Silencio
      if altura != 0:
        """
        Relacion: altura > puntero en el set de intervalos; Trasponer
        dentro del set de intervalos, luego Transportar, sumar a la nota
        resultante.
        """
        n = intervalos[ ( ( altura - 1 ) + transponer ) % len( intervalos ) ] 
        nota = transportar + n
        """
        Armar superposicion de voces.
        """
        if voces:
          for v in voces:
            voz = ( altura + ( v[ paso % len( v ) ] ) - 1 ) + transponer
            acorde += [ transportar +  intervalos[ voz % len( intervalos ) ]  ]

      """
      Cambios de control.
      """
      controles = []
      if capas:
        for capa in capas:
          controles += [ capa[ paso % len( capa ) ] ]

      """
      Articulación a secuenciar.
      """
      articulacion = Articulacion(
         nombre = str( self.orden ) + self.nombre + str( paso ),
         paso  = paso,
         bpm = bpm,
         programa = programa,
         duracion =  duracion,
         dinamica = dinamica,
         nota = nota,
         acorde = acorde,
         tono = tono,
         controles = controles,
      )
      ARTICULACIONES.append( articulacion )
    self.articulaciones = ARTICULACIONES

