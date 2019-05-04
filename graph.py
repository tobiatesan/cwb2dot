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

from process import *
from misc import *

class Node():
    def __init__(self, p, e, name=[]):
        self.color = False
        debug_out(e.__class__)
        assert(e.__class__ == set)
        self.p = p
        self.e = e
        self.name = name
    def __repr__(self):
        return "Node("+str(self.p) +"," +str(self.e)+")"

class Edge():
    def __eq__(self, other):
        if (other.__class__ == Edge and
            other.a == self.a and
            other.n == self.n):
            return True
        return False
    def __hash__(self):
        return hash(self.a) + hash(self.n)
    def __init__(self, a, n, name=[]):
        assert(a is not None)
        assert(isinstance(a, Action))
        assert(n is not None)
        assert(isinstance(n, Node))
        self.a = a
        self.n = n
    def __repr__(self):
        return "--"+str(self.a)+"-->" +str(self.n.p)


def traverse(g):
    visited = list()
    traversal = list()
    import queue
    q = queue.Queue()
    q.put(g)
    visited.append(g)
    while (not q.empty()):
        n = q.get()
        traversal.append(n)
        for e in n.e:
            if(e.n not in visited):
                q.put(e.n)
                visited.append(e.n)
    print("TRAVERSAL")
    for v in visited:
        print("")
        print(v)
    print("END TRAVERSAL OF", len(visited), "NODES")
