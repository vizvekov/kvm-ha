__author__ = 'Vadim'

from mod_loader import import_module


path = 'modules'
names = ["mod1"]

for name in names:
    mod = import_module(path, name, name).mod()
    mod.run()