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

from lark import Lark, Transformer, v_args, Token, Tree
from grammar import cwbgrammar
parser = Lark(cwbgrammar)
from process import *

# All of this is really quite hacky, fix grammar and rewrite it

def do_parse(string):
    # if ((parser.parse(string)) is single agent...
    parsed = parser.parse(string)
    if (parsed.data == "agent"):
        procs = [parsed]
    else:
        assert(parsed.data == "start")
        procs = list(filter(lambda x: x.data == "agent", parser.parse(string).children))

    def descend_substs(tree): # HACK
        assert(len(tree.children) == 2)
        if (tree.data == "subst"):
            return [tree.children]
        else:
            assert (tree.data == "substs")
            substs = [tree.children[0].children]
            return substs + descend_substs(tree.children[1])

    def descend_labels(tree): # HACK
        if (tree.__class__ == Token):
            return [tree]
        assert(tree.__class__ == Tree)
        assert(len(tree.children) == 2)
        if (tree.children[1].__class__ == Token):
            return tree.children
        else:
            labels = [tree.children[0]]
            return labels + descend_labels(tree.children[1])

    def make_forest(tree):
        assert(tree.data == "agent")
        tok0 = tree.children[0]
        assert(tok0.type == "PROCNAME")
        procname = tok0.value
        proc = tree.children[1]
        return (procname, proc)

    # Take all the top level agent statements and turn them into a
    # neat(?) PROCNAME -> Tree dictionary
    ast_dict = dict(list(map(make_forest, procs)))

    def make_proc(proc):
        if (proc.__class__ == Token):
            if (proc.type == "PROCNAME"):
                return KProcess(proc.value)
            else:
                assert(False)
        else:
            assert (isinstance(proc, Tree))
            # No pattern matching in python, so we do this
            def case_chain(proc):
                return ActProcess(make_action(proc.children[0]), make_proc(proc.children[1]))
            def case_rel(proc):
                assert(len(proc.children) == 2)
                assert(proc.children[1].__class__ == Tree)
                orig = make_proc(proc.children[0])
                substs = proc.children[1]
                assert(substs.__class__ == Tree)
                substs = descend_substs(substs)
                subs = set(map(lambda x: Subst(Label(x[1].value), Label(x[0].value)), substs))
                return RelProcess(subs, orig)
            def case_res(proc):
                assert (proc.data == "res")
                assert(len(proc.children) == 2)
                cuts = proc.children[1]
                cuts = descend_labels(cuts)
                orig = make_proc(proc.children[0])
                tocut = set(map(lambda x: Label(x.value), cuts))
                return ResProcess(tocut, orig)
            def case_sum(proc):
                procs = set(map(make_proc, proc.children))
                return SumProcess(procs)
            def case_pipe(proc):
                procs = set(map(make_proc, proc.children))
                return PipeProcess(procs)
            options = {
                "chain": case_chain,
                "rel": case_rel,
                "res": case_res,
                "sum": case_sum,
                "pipe": case_pipe
            }
            return options[proc.data](proc)

    processes = {k: make_proc(v) for k, v in ast_dict.items()}
    return processes, ast_dict
