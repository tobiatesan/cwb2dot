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

# All of this is really quite hacky, fix it and rewrite it along
# with parser...

cwbgrammar = """?start: (stuff)+

?stuff: "agent" PROCNAME "=" process ";" -> agent
      | ignored MOSTSTUFF ";"

?ignored: "branchingeq" | "ccs" | "checkprop" | "model-checking"
       | "checkpropold" | "clear" | "closure" | "cong" | "contraction" | "cwb"
       | "mostly" | "for" | "internal" | "use" | "deadlocks" | "deadlocksobs"
       | "derivatives" | "dfstrong" | "dftrace" | "dfweak" | "diveq"
       | "diverges" | "echo" | "eq" | "findinit" | "findinitobs" | "freevars"
       | "game" | "globalmc" | "graph" | "help" | "init" | "input" | "localmc"
       | "logic" | "mayeq" | "maypre" | "min" | "musteq" | "mustpre" |
       | "normalform" | "obs" | "output" | "pb" | "pre" | "precong" |
       | "prefixform" | "print" | "prop" | "quit" | "random" | "relabel" |
       | "save" | "set" | "sim" | "size" | "sort" | "stable" | "states" |
       | "statesexp" | "statesobs" | "strongeq" | "strongpre" | "testeq" |
       | "testpre" | "toggle" | "transitions" | "twothirdseq" | "twothirdspre"
       | "vs"

?process: relablable "\\\\" "{" labels "}" -> res
        | relablable "[" substs "]" -> rel
        | dprocess

?relablable: PROCNAME
        | "(" process ")"

?dprocess: dprocess "|" dprocess -> pipe
        | cprocess
        | bprocess

?cprocess: cprocess "+" cprocess -> sum
        | bprocess

?bprocess: action "." bprocess -> chain
        | PROCNAME
        | "(" process ")"

?substs: subst
       | subst "," substs

?labels: label
       | label "," labels

?subst: label "/" label

?label: NAME

?action: iaction
       | oaction

?iaction: label -> iaction
?oaction: "'" label -> oaction

COMMENT                 :   "*" /(.)*/ NEWLINE
MOSTSTUFF               :   ("," | "(" | ")" | "=" | /\w/ | " " | /[0-9]/)+
PROCNAME                :   (/[A-Z]/ | /[a-z]/ | /[0-9]/)+"'"*

%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS_INLINE
%import common.NEWLINE

%ignore COMMENT
%ignore WS_INLINE
%ignore NEWLINE"""
