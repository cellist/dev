#!/usr/bin/env python

from pylib import Bonjour

b = Bonjour("Hello, world!")
b.greet()
b.msg = "Bonjour tout le monde"
b.greet()
print( b.msg )
