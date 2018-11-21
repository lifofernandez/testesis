import pygraphviz as pgv

A  = pgv.AGraph(
  bgcolor='#cccccc',
  layout='dot',
  rankdir = 'LR',
  constraint = 'false',
  rank = 'same',
)
# add some edges
A.add_edge(1,2)
A.add_edge(2,3)
A.add_edge(1,3)
A.add_edge(3,4)
A.add_edge(3,6)
A.add_edge(4,5)
A.add_edge(5,6)
# make a subgraph with rank='same'
B = A.add_subgraph(
  [ 4, 5, 6 ], 
  name='cluster_s1',
  #rank='same',
  label='oepe'
)
#B.graph_attr['rank']='same'
B.add_edge(6,'e')
B.add_edge('e','ee')
C = B.add_subgraph( 
  [ 'e' ],
  name = 'cluster_s2',
  #rank='same',
  label='oee'
)
D = B.add_subgraph( 
  [ 'ee', 'ooo' ],
  name = 'cluster_s3',
  #rank='same',
  label='dwee'
)
A.draw( 'Topology.png', prog='dot' )
