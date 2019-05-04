##########################################################################
#                                                                        #
# cwb2dot                                                                #
# Copyright (C) 2019 Tobia Tesan                                         #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
#  along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

from functools import reduce

class Process():
    pass

class KProcess(Process):
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        if (other.__class__ == KProcess and other.name == self.name):
            return True
        return False
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "K("+self.name+")"

class ActProcess(Process):
    def __hash__(self):
        return hash(self.p) + hash(self.act)
    def __eq__(self, other):
        if (other.__class__ == ActProcess and other.act == self.act and other.p == self.p):
            return True
        return False
    def __init__(self, act, p):
        assert(isinstance(act, Action))
        self.act = act
        self.p = p
    def __repr__(self):
        return str(self.act)+"."+str(self.p)

class ResProcess(Process):
    def __hash__(self):
        return (reduce(lambda x,y: x + y, map(hash, self.cut), 0)) + hash(self.p)
    def __eq__(self, other):
        if (other.__class__ == ResProcess and set(other.cut) == set(self.cut) and other.p == self.p):
            return True
        return False
    def __init__(self, cut, p):
        assert(isinstance(cut, set))
        assert(all(isinstance(item, Label) for item in cut))
        assert(isinstance(p, Process))
        self.cut = cut
        self.p = p
    def __repr__(self):
        return "("+str(self.p)+")\{"+", ".join(map(str, self.cut))+"}"

class RelProcess(Process):
    def __hash__(self):
        return (reduce(lambda x,y: x + y, map(hash, self.rel), 0)) + hash(self.p)
    def __eq__(self, other):
        if (other.__class__ == RelProcess and set(other.rel) == set(self.rel) and other.p == self.p):
            return True
        return False
    def __init__(self, rel, p):
        assert(isinstance(rel, set))
        assert(all(isinstance(item, Subst) for item in rel))
        assert(isinstance(p, Process))
        self.rel = rel
        self.p = p
    def __repr__(self):
        return "("+str(self.p)+")["+",".join(map(str, self.rel))+"]"

class SumProcess(Process):
    def __hash__(self):
        return (reduce(lambda x,y: x + y, map(hash, self.procs), 0))
    def __eq__(self, other):
        if (other.__class__ == SumProcess and set(other.procs) == set(self.procs)):
            return True
        return False
    def __init__(self, procs):
        assert(procs.__class__ == set)
        self.procs = procs
    def __repr__(self):
        return " + ".join(map(str, self.procs))

class PipeProcess(Process):
    def __hash__(self):
        return (reduce(lambda x,y: x + y, map(hash, self.procs), 0))
    def __eq__(self, other):
        if (other.__class__ == PipeProcess and set(other.procs) == set(self.procs)):
            return True
        return False
    def __init__(self, procs):
        assert(procs.__class__ == set)
        self.procs = procs
    def __repr__(self):
        return " | ".join(map(str, self.procs))

class Action:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.__unicode__()

class Transition:
    def __hash__(self):
        return (hash(self.p) + hash(self.a) * 2)
    def __eq__(self, other):
        if (other.__class__ == Transition and other.p == self.p and other.a == self.a):
            return True
        return False
    def __init__(self, a, p):
        assert(isinstance(a, Action))
        assert(isinstance(p, Process))
        self.a = a
        self.p = p
    def __repr__(self):
        return "--" + str(self.a) + "-->" + str(self.p)

class WeakTransition:
    def __hash__(self):
        return (hash(self.p) + hash(self.a) * 3)
    def __eq__(self, other):
        if (other.__class__ == WeakTransition and other.p == self.p and other.a == self.a):
            return True
        return False
    def __init__(self, a, p):
        assert(isinstance(a, Action))
        assert(isinstance(p, Process))
        self.a = a
        self.p = p
    def __repr__(self):
        return "==" + str(self.a) + "==>" + str(self.p)

class IAction (Action):
    def __hash__(self):
        return hash(self.label)*2
    def __eq__(self, other):
        if (other.__class__ == IAction and other.label == self.label):
            return True
        return False
    def __init__(self, label):
        self.label = label
    def __unicode__(self):
        return (""+self.label.name)


class OAction (Action):
    def __hash__(self):
        return hash(self.label)*3
    def __eq__(self, other):
        if (other.__class__ == OAction and other.label == self.label):
            return True
        return False
    def __init__(self, label):
        self.label = label
    def __unicode__(self):
        return ("'"+self.label.name)

class TauAction (Action):
    def __hash__(self):
        return 111133332222333322222
    def __eq__(self, other):
        if (other.__class__ == TauAction):
            return True
        return False
    def __init__(self):
        pass
    def __unicode__(self):
        return ("tau")

def make_action(tree):
    if (tree.data == "iaction"):
        return IAction(Label(tree.children[0].value))
    else:
        if (tree.data == "oaction"):
            return OAction(Label(tree.children[0].value))
        else:
            assert(False)

class Subst():
    def __init__(self, fro, to):
        assert(fro.__class__ == Label)
        assert(to.__class__ == Label)
        self.fro = fro
        self.to = to
    def __unicode__(self):
        return self.fro.name+"|->"+self.to.name
    def __repr__(self):
        return self.__unicode__()

class Label():
    def __hash__(self):
        return hash(self.name)
    def __ne__(self, other):
        return not (self.__eq__(other))
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False
    def __init__(self, name):
        assert(name.__class__ == str)
        self.name = name
    def __unicode__(self):
        return ("l("+self.name+")")
    def __repr__(self):
        return self.__unicode__()
