import sys

def flip(edge):
    return (edge[1],edge[0])

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
    n = t
    while n != s:
        path.append((prev[n],n))
        n = prev[n]
    path
    path.reverse()
    return path

# pass-by-reference
def augment(g, p):
    weight = max(g.values())
    # compute the bottleneck
    for e in p:
        weight = min(weight, g[e])
    for e in p:
        g[e] -= weight
        g[flip(e)] += weight


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

def max_flow(G, s, t):
    # create a reference copy of G
    Ref = { edge: G[edge] for edge in G.keys() }
    # compute delta
    delta = compute_delta(G, s)

    while delta >= 1:
        # this is scaling
        p = scaled_s_t_path(G, delta, s, t)
        while p != []:
            augment(G, p)
            p = scaled_s_t_path(G, delta, s, t)
        delta /= 2

    # this is the flow
    return {edge : Ref[edge] - G[edge] for edge in Ref.keys() if Ref[edge] > 0}

def main():
    G = {}
    s, t = 0, 0 # source and sink, introducing their varnames
    for line in sys.stdin:
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
            edge = (int(words[1]), int(words[2]))
            assert edge not in G and flip(edge) not in G
            G[edge] = float(words[3])
            G[flip(edge)] = 0

    print max_flow(G, s, t)

main()
