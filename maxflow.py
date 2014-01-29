import sys
from collections import defaultdict

# This is a re-write of the max-flow algorithm, but it's very similar.
# The biggest change is that G is a dict-of-dicts, and actually defaultdict.
# That means if we rvalue G[u] without u being in G yet, it automatically
# initializes G[u] = {}, and if G[u][v] has the same, G[u][v] = 0.
# This is all just for short-hand. Still, gives us a good "adjacency list".

def read_graph(infile):
    # correct syntax thanks to http://stackoverflow.com/questions/5029934/python-defaultdict-of-defaultdict
    G = defaultdict(lambda : defaultdict(float))
    s, t = 0, 0
    # load up the graph
    for line in infile: 
        words = line.split()
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
            # DIMACS does not disallow parallel edges. However,
            # we automatically combine such edges. Otherwise,
            # we're standard.
            u = int(words[1])
            v = int(words[2])
            weight = float(words[3])
            G[u][v] += weight

    return G, s, t

# iterator over edges of graph
def edges(graph):
    for u in graph.keys():
        for v in graph[u]:
            yield (u,v)

# dumb utility
def compute_delta(G,s):
    maxweight = max(G[s].values())
    delta = 1
    while delta * 2 < maxweight: delta *= 2
    return delta

# find and generate an augmenting path in G,
# further constrained that all the edges have
# a "high enough" weight.
def scaled_s_t_path(G, delta, s, t):
    wq  = [s] # workqueue
    seen = set([s])
    prev = {}
    while wq:
        u = wq.pop()
        for v in G[u]:
            if v not in seen and G[u][v] >= delta:
                seen.add(v)
                prev[v] = u
                if v == t:
                    break
                wq.append(v)
    path = []
    if t not in prev: return path

    v = t
    while v != s:
        path.append((prev[v], v))
        v = prev[v]
    path.reverse()
    return path

# given an augmenting path, push as much flow as
# possible throguh it.
def augment(G, P):
    # the map makes a list of all edge-weights in P
    bottleneck = min(map(lambda e : G[e[0]][e[1]], P))
    for u, v in P:
        G[u][v] -= bottleneck
        G[v][u] += bottleneck
    

# Our scaling max-flow! Observe that R is a different
# map type: it maps (u,v) -> weight, no adjacency structure.
def max_flow(G, s, t):
    R = { edge : G[edge[0]][edge[1]] for edge in edges(G) }
    delta = compute_delta(G,s)
    while delta >= 1:
        augpath = scaled_s_t_path(G, delta, s, t)
        while augpath != []:
            #print augpath, min(map(lambda e : G[e[0]][e[1]], augpath))
            augment(G, augpath)
            augpath = scaled_s_t_path(G, delta, s, t)
        delta /= 2

    return { e : R[e] - G[e[0]][e[1]] for e in R.keys() if R[e] >= G[e[0]][e[1]]}

# prints out the DIMACs-formatted description of our solution flow
def dimacs_print_flow(F,s):
    totflow = 0
    for e in F:
        if e[0] == s:
            totflow += F[e]
    print 'c solving max flow'
    print 'c using agorenst python solver'
    print 'c'
    print 's', totflow
    print 'c'
    print 'c Source Dest Flow'
    # just making things sorted, pretty
    sortedF = sorted(list(F.keys()))
    for e in sortedF:
        print 'f', e[0], e[1], F[e]
    print 'c'
    print 'c End'


if __name__=="__main__":
    G, s, t = read_graph(sys.stdin)
    F = max_flow(G, s, t)
    dimacs_print_flow(F, s)
