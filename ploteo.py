from datetime import datetime, timedelta
from main import PARTES, formato_tiempo
import matplotlib.pyplot as ploter
import numpy as np
import matplotlib.dates as mdates

print( '#### PLOTEANDO ####' )
for parte in PARTES:
  grafico, eje_x = ploter.subplots( figsize = ( 8, 5 ) )
  levels = np.array( [-5, 5, -3, 3, -1, 1] )
  start = parte[ 'comienzo' ]
  track = parte[ 'orden' ]
  dimension = parte[ 'duracion' ]
  stop  =  dimension
  eje_x.plot( 
    ( start, stop ),
    ( 0, 0 ),
    'k',
    alpha = .5
  )
  eje_x.set( title = parte[ 'nombre' ] )

  for index, etiqueta in enumerate( parte[ 'etiquetas'] ):
    m = etiqueta[ 'cuando' ] 
    t = str( timedelta( seconds = m ) )
    t = t.split('.')[0] # borra microsegundos
    idate = datetime.strptime( t , formato_tiempo) 
    level = levels[ index % 6 ]
    vert = 'top' if level < 0 else 'bottom'
    eje_x.scatter(
      idate,
      0,
      s = 100,
      facecolor = 'w',
      edgecolor = 'k',
      zorder = 9999
     )
     # Plot a line up to the text
    eje_x.plot(
      ( idate, idate ), 
      ( 0, level ), 
      c = 'r', 
      alpha = .7
    )
    # Give the text a faint background and align it properly
    eje_x.text(
       idate,
       level,
       etiqueta['texto'],
       horizontalalignment = 'right',
       verticalalignment = vert,
       fontsize = 14,
       backgroundcolor = ( 1., 1., 1., .3 )
    )
    # TODO: Agregar etiqueta al final dela parte
    #momento += evento[ 'duracion' ] 

  # Set the x ticks formatting
  # format x axis with 3 second intervals
  eje_x.get_xaxis().set_major_locator( mdates.SecondLocator( interval = 3 ) )
  eje_x.get_xaxis().set_major_formatter( mdates.DateFormatter( "%M %S" ) )
  grafico.autofmt_xdate()
  # Remove components for a cleaner look
  ploter.setp( 
    (
      eje_x.get_yticklabels() + 
      eje_x.get_yticklines() +
      list( eje_x.spines.values() )
    ),
    visible = False
  )
ploter.show()
