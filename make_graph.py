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
