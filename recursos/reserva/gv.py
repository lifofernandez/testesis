from graphviz import Digraph

grafico = Digraph(
  'G',
  filename = 'cluster.gv'
)
grafico.graph_attr[ 'rankdir' ] = 'LR'
grafico.graph_attr[ 'constraint' ] = 'false'
grafico.graph_attr[ 'rank' ] = 'same'

zero = Digraph( name = 'cluster_0' )
zero.attr( 
  color = 'blue',
  label = 'process #0'
)
uno = Digraph( name = 'cluster_1' )
uno.attr( 
  style = 'filled',
  rank = 'same',
  rankdir = 'LR',
  color = 'red',
  constraint = 'false',
  label = 'process #1'
)
uno.edges( [
  ( 'a0', 'a1' ),
  ( 'a1', 'a2' ),
  ( 'a2', 'a3' )
] )
zero.subgraph( uno )

dos = Digraph( 'cluster_2' )
dos.attr( 
  style = 'filled',
  rank = 'same',
  rankdir = 'LR',
  color = 'pink',
  constraint = 'false',
  label = 'process #2'
)
dos.edges( [
  ( 'b0', 'b1' ),
  ( 'b1', 'b2' ),
  ( 'b2', 'b3' )
] )

tres = Digraph( name = 'cluster_3' )
tres.attr( 
  style = 'filled',
  rank = 'same',
  rankdir = 'LR',
  color = 'yellow',
  constraint = 'false',
  label = 'process #3'
)

tres.edges( [
  ( 'c0', 'c1' ),
  ( 'c1', 'c2' ),
  ( 'c2', 'c3' )
] )

tres.edges( [
  ( 'cc0', 'cc1' ),
] )
dos.subgraph( tres )

dos.edges( [
  ( 'c3', 'd3' )
] )




zero.subgraph( dos )

grafico.edges( [
  ( 'a3', 'b0' ),
  ( 'b3', 'c0' )
] )

grafico.subgraph( zero )

grafico.view( )

