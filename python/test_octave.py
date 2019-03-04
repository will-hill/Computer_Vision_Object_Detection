import oct2py

o = oct2py.Oct2Py()
o.addpath(o.genpath('../octave/'))
opts = o.acfTrain()

o.eval('clc')
o.eval('clear')
o.eval('addpath(genpath("../octave"))')

print('finito')
