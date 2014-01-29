maxflow
=======

Educational implementation of the max flow algorithm in Python

The max-flow algorithms as presented in theory textbooks build up a lot of (necessary!) conceptual objects like the residual graph, the flow, and so on.
These structures are fairly involved, and may intimidate students into thinking that a max-flow algorithm is very difficult to implement.
However, it is important to understand which objects are necessary for the algorithm _implementation_, and which are only for understanding.

In this simple Python implementation of the scaling max-flow algorithm as shown in the K&T, you can see that in fact the algorithm's structure is fairly simple.
Of course, one can't trust it works without analytical tools like the residual graph, but the executing code doesn't care about those.
This is __not__ built with efficiency in mind. It runs much more slowly than freely (and easily!) available algorithms on the internet.
Rather, the goal is to provide a nice, happy, simple implementation, to perhaps show some students that implementing even max-flow is quite feasible.

Files
-----

Only two real files, you feed maxflow.py a DIMACS file via stdin and it spits out the solution via stdout.
If you're concerned, the verify.py script can make sure that the purported flow at least satisfies conservation and capacity constraints.

Resources
=========

The DIMACS format (describing the input and output formats) is fairly straightforward, and is defined at [this sourceforge site](http://lpsolve.sourceforge.net/5.5/DIMACS_maxf.htm).
It is not a perfectly precise specification (in particular, does it dis-allow repeated edges? Parallel edges?)
The DIMACS website may have originally hosted the specification and some benchmarks, but it appears to have been taken down sometime over the last decade.


Some input examples I found about the internet: (Apparently vision people really like this algorithm!)
A researcher from [U Chicago](http://ttic.uchicago.edu/~dbatra/research/mfcomp/) has some absolutely huge data-sets.
For these, even the 11MB files will make my implementation very sad.
Don't bother testing mine with them, haha.
A group page from [U Western](http://vision.csd.uwo.ca/maxflow-data) has some much more manageable vision inputs.

If you want to actually just solve DIMACS-formatted max-flow problems in a general programming language, I would suggest [boost](http://www.boost.org/doc/libs/1_46_1/libs/graph/example/boykov_kolmogorov-eg.cpp).
