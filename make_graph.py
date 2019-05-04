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
from ccs import *
from graph import *
def make_graph(processname, processes, weak=False, normalization=True):
    # normalization = True makes examples/boom.cwb collapse into agent
    # BOOM = 'ping.BOOM --i.e. [pong/ping] is ignored since pong is
    # not in the actions for boom.
    debug_out("Graphing for " + processname)
    p = KProcess(processname)
    visited = dict()
    traversal = list()
    import queue
    q = queue.Queue()
    q.put(p)
    visited[p] = Node(p, set())
    g = visited[p]
    edges = 0
    while (not q.empty()):
        p = q.get()
        debug_out ("Visiting " + str(p))
        if (normalization == True):
            p = normalize(p, processes)
        debug_out ("Normalizes to " + str(p))
        if (weak):
            acs = weak_transitions(p, processes)
        else:
            acs = transitions(p, processes)
        debug_out ("Has transitions " + str(acs))
        for transition in acs:
            act, proc = (transition.a, transition.p)
            if (normalization == True):
                proc = normalize(proc, processes)
            if(proc not in visited.keys()):
               debug_out(str(proc) + " not in " + str(visited.keys()))
               visited[proc] = Node(proc, set())
               q.put(proc)
            visited[p].e.add(Edge(act, visited[proc]))
            edges += 1
    debug_out ("Made ", edges, " edges")
    return g
