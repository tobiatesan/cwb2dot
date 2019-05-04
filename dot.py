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

from graphviz import Digraph
from dot import *
from misc import *

from process import KProcess
# TODO Decouple

def graph_to_dot(graph, title):
    dot = Digraph(comment=title)
    import queue
    q = queue.Queue()
    done = list()
    doneedge = list()
    q.put(graph)
    counter = 0
    edges = 0
    recount = 0
    legend = dict()
    while (not q.empty()):
        n = q.get()
        debug_out("Doing ", n)
        debug_out("Has hash", hash(n))
        debug_out("Has const hash", hash(n))
        debug_out("Already done:", done)
        if (not hash(n) in done):
            if (n.p.__class__ == KProcess):
                # TODO: Shouldn't know about this
                name = n.p.name
                dot.node("n"+str(hash(n)), name)
            else:
                dot.node("n"+str(hash(n)), str(counter + 1))
            legend[counter] = n.p
            done += [hash(n)]
            counter += 1
            recount += len(n.e)
            for edge in n.e:
                if (not hash(edge.n) in done):
                    q.put(edge.n)
                debug_out("Adding edge ", edge)
                dot.edge("n"+str(hash(n)), str("n"+str(hash(edge.n))), str(edge.a))
                edges += 1
                doneedge += [hash(edge)]
    debug_out("Counted ", counter, "nodes")
    debug_out("Counted ", edges, "edges")
    debug_out("Seen ", recount, "edges")
    debug_out("Marked ", len(doneedge), "edges")
    debug_out(legend)
    return (dot, legend)
