from functools import reduce
from graphviz import Digraph
from functools import reduce
from sys import argv
import sys
import argparse

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass

from misc import debug_out
from process import *
from parser import *
from ccs import *
from graph import *
from dot import *
from make_graph import make_graph

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help="A CWB script", type=str)
    parser.add_argument('operation', choices=["listagents", "printgraph", "previewgraph", "transitions"])
    parser.add_argument('--weak', action='store_true', help="Use it to print weak transitions")
    parser.add_argument('--agent', type=str, help="Must be specified for printgraph and transitions")
    parser.add_argument('--debug', type=str, help="Print extra debug information")
    args = parser.parse_args()

    source = args.input_file
    operation = args.operation

    with open(source, 'r') as file:
        string = file.read()
    processes, asts = do_parse(string)

    if (operation == "listagents"):
        print("Agents found:\n")
        count = 1
        for name in processes:
            print(str(count) + ") " + name)
            count += 1
        print("\n=====================\n")
        transitions_ = lambda x: transitions(x, processes)
        findlabels = lambda x: find_all_labels(x, processes)
        if (args.debug):
            print("About each of them...\n")
            for name in processes:
                ast = asts[name]
                proc = processes[name]
                print("AST("+name+") = " + str(ast))
                print("A("+name+ ") = "+ str(transitions_(proc)))
                print("L("+name+ ") = "+ str(findlabels(proc)))
    else:
        agent = args.agent
        if (agent is None):
            print("Must specify an agent! Try listagents")
            sys.exit(-1)
        if (agent not in processes.keys()):
            print("No such agent", agent)
            sys.exit()
        if (operation == "transitions"):
            if (not args.weak):
                transitions_ = lambda x: weak_transitions(x, processes)
            else:
                transitions_ = lambda x: transitions(x, processes)
            findlabels = lambda x: find_all_labels(x, processes)
            proc = processes[agent]
            print("A("+agent+ ") = "+ str(transitions_(proc)))
            print("L("+agent+ ") = "+ str(findlabels(proc)))
        if (operation in ["printgraph", "previewgraph"]):

            if (args.weak):
                g = make_graph(agent, processes, True)
            else:
                g = make_graph(agent, processes)

            (dot, legend) = graph_to_dot(g, "Title")
            if (operation == "printgraph"):
                print(dot.source)
            else:
                assert(operation == "previewgraph")
                dot.render('/tmp/cwb.gv', view=True)
