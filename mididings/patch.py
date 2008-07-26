# -*- coding: utf-8 -*-
#
# mididings
#
# Copyright (C) 2008  Dominic Sacré  <dominic.sacre@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

import _mididings
import units


class Patch(_mididings.Patch):
    def __init__(self, p):
        _mididings.Patch.__init__(self, self.build(p))

    def build(self, p):
        if isinstance(p, units._Chain):
            v = Patch.ModuleVector()
            for i in p.items:
                v.push_back(self.build(i))
            return Patch.Chain(v)

        elif isinstance(p, list):
            v = Patch.ModuleVector()
            for i in p:
                v.push_back(self.build(i))
            return Patch.Fork(v)

        elif isinstance(p, dict):
            return self.build([
                units.Filter(t) >> w for t, w in p.items()
            ])

        elif isinstance(p, units._Unit):
            return Patch.Single(p)

        # whoops...
        raise TypeError('invalid patch')
