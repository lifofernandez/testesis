#from setuptools import setup, find_packages
from setuptools import setup
# you may need setuptools instead of distutils

setup(
    name             = 'yml2mid',
    version          = '0.1',
    description      = 'Compose MIDI sequences using YAML definitions.',
    author           = 'Man Foo',
    author_email     = 'foomail@foo.com',
    packages         = ['yml2mid'],  #same as name
    #packages         = find_packages(),
    install_requires = [
      'pyyaml',
      'midiutil',
    ]
    scripts = [
      'argumentos.py',
      'articulacion.py',
      'elemento.py',
      'main.py',
      'pista.py',
      'seccion.py',
      'segmento.py',
      'yml2mid',
    ]
)

