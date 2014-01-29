import sys
from collections import defaultdict

if len(sys.argv) != 3:
    print "Usage: ./python verify graphfile.max flowfile"
    sys.exit(0)
graphfile = open(sys.argv[1])
flowfile = open(sys.argv[2])

def read_graph(infile):
    G = defaultdict(lambda : defaultdict(float))
    s, t = 0, 0
    # load up the graph
    for line in infile:
        words = line.split()
        if len(words) == 0:
            continue
        if words[0] == 'c': # comment, ignore
            pass
        if words[0] == 'p': # p max-flow, num_nodes, num_edges. Ignore: we're dynamic
            pass
        if words[0] == 'n': # node ID source/sink
            assert words[2] == 's' or words[2] == 't'
            assert int(words[1]) > 0
            if words[2] == 's':
                s = int(words[1])
            else:
                t = int(words[1])
        if words[0] == 'a': # edge(arc) in out weight
            # what about repeated edges? flipped eges in the input file?
            u = int(words[1])
            v = int(words[2])
            weight = float(words[3])
            G[u][v] += weight

    return G, s, t

G, s, t = read_graph(graphfile)

# measure the out and inflow to each vertex
Out = defaultdict(float)
In = defaultdict(float)
for line in flowfile:
    words = line.split()
    if len(words) == 0:
        continue
    if words[0] == 'f':
        u, v = map(int,words[1:3])
        w = float(words[3])

        # check capacity!
        if w > G[u][v]:
            print "Error with edge:", u, v, "assigned flow", w, "with capacity", G[u][v]

        Out[u] += w
        In[v] += w

# this will only give us nodes with outgoing edges
# (ie, the sink node should NOT be included in the iteration to begin with.)
for u in G.keys():
    if Out[u] != In[u] and u != s:
        print "Error, conservation violated for", u, ": Out:", Out[u], "In:", In[u]

if Out[s] != In[t]:
    print "Error, outflow from source is not equal to inflow to sink!", s, t, Out[s], In[t]


print 'Done! If no errors printed, it passed capacity and conservation checks'
