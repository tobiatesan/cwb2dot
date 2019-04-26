
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

?process: relablable "\\\\ {" labels "}" -> res
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

COMMENT                 :   "*" /(.)+/ NEWLINE
MOSTSTUFF               :   ("," | "(" | ")" | "=" | /\w/ | " " | /[0-9]/)+
PROCNAME                :   (/[A-Z]/ | /[a-z]/ | /[0-9]/)+"'"*

%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS_INLINE
%import common.NEWLINE

%ignore COMMENT
%ignore WS_INLINE
%ignore NEWLINE"""
