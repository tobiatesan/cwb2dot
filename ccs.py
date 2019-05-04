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

def weak_cont(proc, const, visited):
    # TODO nroam
    proc = normalize(proc, const)
    acs = transitions(proc, const)
    taus = filter(lambda pair:
                  pair.a.__class__ == TauAction,
                  transitions(proc, const))
    return reduce(set.union,
                  map(lambda x: weak_cont(normalize(x.p, const),
                                          const,
                                          visited+[normalize(x.p, const)]),
                      filter(
                          # Avoid infinite recursion in case of
                          # tau actions that loop to self
                          lambda x: normalize(x.p, const) not in visited,
                          taus
                      )
                  ),
                  set().union([proc]))

def weak_transitions(proc, const, visited=[]):
    # P =a=> Q holds iff  P (-tau->)* -a-> (-tau->)* Q
    proc = normalize(proc, const)
    acs = transitions(proc, const)
    taus = filter(lambda x: x.a.__class__ == TauAction,
                  acs)
    not_taus = filter(lambda x: x.a.__class__ != TauAction, acs)

    # Taus might be the first tau-part of a weak transition, see where they lead.
    # We get FULL WEAK TRANSITIONS in return

    # From not-taus might start the second tau-part, possibly zero-long, of a weak transition
    # weak_cont gives us PROCESSES

    rec = reduce(set.union,
                 map(lambda x: weak_transitions(normalize(x.p, const),
                                            const,
                                            visited+[normalize(x.p, const)]),
                     filter(lambda x: normalize(x.p, const)
                            not in visited,
                            taus)
                 ),
                 set())

    return reduce(
        set.union,
        map(lambda x:
            map(lambda y:
                WeakTransition(x.a, y),
                weak_cont(normalize(x.p, const), const, [normalize(x.p, const)]))
            , filter(lambda x: normalize(x.p, const) not in visited,
                     not_taus)),
        rec)


def transitions(proc, const):
    debug_out ("Finding transitions for", proc)
    transitions2 = lambda x: transitions(x, const)
    assert(isinstance(proc, Process))
    def case_chain(proc):
        return {Transition(proc.act, proc.p)}
    def case_ren(proc):
        a = transitions2(proc.p)
        assert(isinstance(a, set))
        assert(all(isinstance(item, Transition) for item in a))
        def do_subst(action, renamings):
            assert(isinstance(action, Action))
            if (action.__class__ in [IAction, OAction]):
                def do_renaming(action, renaming):
                    assert(isinstance(action, Action))
                    assert(renaming.fro.__class__ == Label)
                    if (action.label == renaming.fro):
                        a = action.__class__(renaming.to)
                        assert(isinstance(a, Action))
                        return a
                    else:
                        assert(isinstance(action, Action))
                        return action
                newaction = reduce(do_renaming, renamings, action)
                assert(isinstance(newaction, Action))
                return newaction
            else:
                return action
        return set(
            map(lambda x: Transition(do_subst(x.a, proc.rel),
                           RelProcess(proc.rel, x.p))
                , a))
    def case_res(proc):
        a = transitions2(proc.p)
        assert(isinstance(a, set))
        assert(all(isinstance(item, Transition) for item in a))
        return set(
            filter(lambda x: isinstance(x.a, TauAction) or x.a.label not in proc.cut,
                   map(lambda x: Transition(x.a,
                        ResProcess(proc.cut, x.p)), a)))

    def case_sum(proc):
        prox = list(map(transitions2, proc.procs))
        res = set().union(*prox)
        return res

    def case_pipe(proc):
        def matches(a,b):
            assert(isinstance(a, Action))
            assert(isinstance(b, Action))
            if(isinstance(a, IAction) and isinstance(b, OAction) and a.label == b.label):
                return True
            if(isinstance(a, OAction) and isinstance(b, IAction) and a.label == b.label):
                return True
            return False
        prox = list(proc.procs)
        assert(len(prox) == 2)
        # Extension comes later
        p0 = prox[0]
        p1 = prox[1]
        a0 = transitions2(p0)
        a1 = transitions2(p1)
        assert(isinstance(a0, set))
        assert(all(isinstance(item, Transition) for item in a0))
        assert(isinstance(a1, set))
        assert(all(isinstance(item, Transition) for item in a1))
        com3 = list(
            map(lambda x: Transition(TauAction(),  PipeProcess({x[0].p, x[1].p})),
            filter(lambda x: matches(x[0].a, x[1].a), [(left,right) for left in a0 for right in a1])
            )
        )
        return set(list(map(lambda x: Transition(x.a, PipeProcess({x.p, p1})), a0)) +
                list(map(lambda x: Transition(x.a, PipeProcess({p0, x.p})), a1)) +
                com3)

    options = {
        ActProcess: case_chain,
        RelProcess: case_ren,
        ResProcess: case_res,
        SumProcess: case_sum,
        PipeProcess: case_pipe,
        KProcess: lambda x: transitions2(const[x.name]),
    }
    return options[proc.__class__](proc)

def find_all_labels(proc, const, colored=set()):
    def case_chain(proc):
        return {proc.act.label}.union(find_all_labels(proc.p, const, colored))
    def case_ren(proc):
        labels = find_all_labels(proc.p, const, colored)
        for rename in proc.rel:
            labels = set({label if label != rename.fro else rename.to for label in labels})
        return labels
    def case_res(proc):
        return {x for x in find_all_labels(proc.p, const, colored) if x not in proc.cut}
    def case_sum(proc):
        return set().union(*map(lambda y: set(find_all_labels(y, const, colored)), proc.procs))
    def case_pipe(proc):
        return set().union(*map(lambda y: set(find_all_labels(y, const, colored)), proc.procs))
    def case_const(proc):
        if (proc not in colored):
            return find_all_labels(const[proc.name], const, colored.union({proc}))
        else:
            return set()
    options = {
        ActProcess: case_chain,
        RelProcess: case_ren,
        ResProcess: case_res,
        SumProcess: case_sum,
        PipeProcess: case_pipe,
        KProcess: case_const,
    }
    return options[proc.__class__](proc)


def normalize(proc, constants):
    # TODO: make this _really_ normalizing...
    def case_rel(proc):
        relabeled = {x.fro for x in proc.rel}
        if (not find_all_labels(proc.p, constants).intersection(relabeled)):
            # Avoid (P)[a->b][a->b]
            return normalize(proc.p, constants)
        else:
            return proc
    def case_res(proc):
        if (not find_all_labels(proc.p, constants).intersection(proc.cut)):
            # Avoid (P)\{l}\{l}\{l}...
            return normalize(proc.p, constants)
        else:
            return proc
    options = {
        ActProcess: lambda x: ActProcess(x.act, normalize(x.p, constants)),
        RelProcess: case_rel,
        ResProcess: case_res,
        SumProcess: lambda x: SumProcess(set(map(lambda x: normalize(x, constants), x.procs))),
        PipeProcess: lambda x: PipeProcess(set(map(lambda x: normalize(x, constants), x.procs))),
        KProcess: lambda x: x,
    }
    return options[proc.__class__](proc)


def resolve_const(proc, processes):
    if (proc.__class__ == KProcess):
        res = processes[proc.name]
        proc = normalize(proc, processes)
        res = normalize(res, processes)
        if (res == proc):
            # Don't circ
            return res
        else:
            return resolve_const(res, processes)
    else:
        return proc
