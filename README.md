maxflow
=======

Educational implementation of the max flow algorithm in Python

Some input examples I found about the internet: 
http://ttic.uchicago.edu/~dbatra/research/mfcomp/ (BIG!)

Point of confusion regarding DIMACS format: are repeated edges, or flipped edges, allowed? What about negative capacities?
Ie, if it says
a 1 2 4
a 2 1 2

does that really mean
a 1 2 2 ?

PS If you actually want to solve a DIMACS-formatted thing (and perhaps this may help answer my question---though I'm not sure how the above website formats things),
I suppose I would just recommend BOOST: http://www.boost.org/doc/libs/1_46_1/libs/graph/example/edmonds-karp-eg.cpp
