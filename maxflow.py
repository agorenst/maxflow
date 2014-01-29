import sys

# Currently, we read in graphs in the DIMACS format 
# (eg http://lpsolve.sourceforge.net/5.5/DIMACS_maxf.htm)
#
# Our graph model is a map from edges (tuples) to weights (doubles)
# This is a fairly inefficient model, but it is quick and easy and works
#
# The algorithm is the K&T scaling algorithm
# Concerns: correctness (not heavily tested), efficiency (in graph representation)
# and numerical correctness (what if values are crazy floats and so forth)
#
# Nice simple input: http://ttic.uchicago.edu/~dbatra/research/mfcomp/

def flip(edge):
    return (edge[1],edge[0])

# we want the highest power of two that's upper-bounded
# by an outgoing edge from s. (we could also bound by
# every edge in G, but this is a cheap-and-easy improvement)
def compute_delta(G, s):
    max_weight = 0
    for e in outgoing_edges(G, 0, s):
        max_weight = max(max_weight, G[e])
    delta = 1
    while delta*2 < max_weight:
        delta *= 2
    return delta

# we have delta, the scaling factor,
# so we can treat g as its delta-scaled form
def outgoing_edges(g, delta, u):
    for edge in g.keys():
        if edge[0] == u and g[edge] > delta:
            yield edge

# returns an implicit BFS tree.
# maybe change into returning the path proper?
def scaled_s_t_path(g, delta, s, t):
    wq = [s]
    seen = set([s])
    prev = {}
    while wq: # this as apparently the python way!
        u = wq.pop(0)
        for e in outgoing_edges(g, delta, u):
            n = e[1]
            #print 'found', n, 'via node', u, 'with weight:', g[(u,n)]
            if n not in seen:
                seen.add(n)
                prev[n] = u
                if n == t:
                    break
                wq.append(n)

    # now we do nice processing to make prev worth our while
    path = []
    if t not in prev:
        return path

    # work backwards to construct the explicit path from s to t
    n = t
    while n != s:
        path.append((prev[n],n))
        n = prev[n]
    path.reverse()
    return path

# pass-by-reference
# Short, but important! Can't get anything wrong here.
def augment(g, p):
    # compute the bottleneck
    # we set weight to max possible, then restrict according to p
    weight = max(g.values())
    for e in p:
        weight = min(weight, g[e])

    # this is actually applying the flow.
    for e in p:
        g[e] -= weight
        g[flip(e)] += weight

# The main function!
# Note that the scaling is implemented "in-line" via
# the delta parameter in scaled_s_t path
def max_flow(G, s, t):
    # create a reference copy of G
    Ref = { edge: G[edge] for edge in G.keys() }
    # compute delta
    delta = compute_delta(G, s)

    while delta >= 1:
        print 'delta:', delta
        p = scaled_s_t_path(G, delta, s, t)
        while p != []:
            augment(G, p)
            p = scaled_s_t_path(G, delta, s, t)
        delta /= 2

    # this is the flow, only include edges with flow!
    return {edge : Ref[edge] - G[edge] for edge in Ref.keys() if Ref[edge] - G[edge] > 0}

# returns graph G, source s, sink t, having read in their
# description from a DIMACS-formatted file.
def dimacs_read_graph(infile):
    G = {}
    s, t = 0, 0 # source and sink, introducing their varnames
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
            # what about repeated edges? flipped eges in the input file?
            edge = (int(words[1]), int(words[2]))
            weight = float(words[3])
            # is this assert valid re: DIMACS format?
            assert edge not in G and flip(edge) not in G:
            G[edge] = weight
            G[flip(edge)] = 0
    return G, s, t

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
        print e[0], e[1], F[e]
    print 'c'
    print 'c End'

# read in the file from stdin, print out the result to stdout
def main():
    G, s, t = dimacs_read_graph(sys.stdin)
    F = max_flow(G, s, t)
    dimacs_print_flow(F,s)

if __name__=="__main__":
    main()
