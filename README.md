# cwb2dot

`cwb2dot` is a quick and rather dirty tool I wrote when faced with the need to prepare a LaTeX document in which I wished to include transition diagrams for my [Edinburgh Concurrency Workbench](http://homepages.inf.ed.ac.uk/perdita/cwb/) agents/processes.

To the best of my knowledge the CWB has no native visualization tool
except for a bridge to DaVinci, which will only export the diagram it
produces to a raster BMP file; similarly [Edinburgh Concurrency
Workbench](http://http://caal.cs.aau.dk/) will only export to raster
PNG files -- i.e. they're both rather LaTeX-unfriendly.

`cwb2dot` will parse your CWB files and produce `dot` files for the strong and weak transition diagrams.
You can render those with [GraphViz](https://www.graphviz.org/) and use the very many tools there are to work with `.dot` files.

Notably, you can also use [dot2tex](https://ctan.org/pkg/dot2tex?lang=en) to turn said files into TiKZ diagrams that you can include in your LaTeX document.

## Usage
Clone the repository:
```
git clone https://github.com/tobiatesan/cwb2dot.git && cd cwb2dot
```
Install the requirements in your Python path (consider using a VirtualEnv):
```
pip install -r ./requirements
```

You can now preview the graph for an agent like this:

```
python3 cwb2dot.py examples/example.cwb previewgraph --agent EXAMPLE
```

Where `examples/example.cwb` is your CWB file and `EXAMPLE` is the name of an agent defined therein with the `agent EXAMPLE` command.
This produces the diagram of strong transitions; you can use the flag `--weak` to get weak transitions.

You can print the dot-source to stdin like this:

```
python3 main.py examples/example.cwb printgraph --agent EXAMPLE
```

You can also save the dot-source to a file via redirection....


```
python3 main.py examples/example.cwb printgraph --agent EXAMPLE > example.dot
```
...and then use dot2tex to render it:

```
dot2tex -ftikz --prog=neato example.dot | pdflatex --jobname example
```

Or, in one go:

```
cat examples/example.cwb  | python3 cwb2dot.py /dev/stdin printgraph --agent EXAMPLE | dot2tex -ftikz --prog=neato /dev/stdin | pdflatex --jobname example
```

Note that dot2tex will gladly give you only the TiKZ source with the `--figonly` option, like this:

```
python3 main.py examples/example.cwb printgraph --agent EXAMPLE | dot2tex -ftikz --figonly --prog=neato /dev/stdin > fig.tikz
```

## Requirements
- Python 3
- [argparse](https://pypi.org/project/argparse/)
- [graphviz](https://pypi.org/project/graphviz/)
- [Lark](https://pypi.org/project/lark-parser/)

## TODO
  - It's very unidiomatic Python. Turn it into idiomatic Python or just rewrite it in Haskell...
  - Implement sane command line options
  - Clean up grammar and parser...
  - Wait for bugs to pop up
  - If sufficiently bored, turn it into a real verification tool -- i.e. implement algorithms to compute equivalence, etc?

## License
`cwb2dot` is released under the GPLv3 License
