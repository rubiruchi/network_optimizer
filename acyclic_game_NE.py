#%%

import numpy
import networkx


def runRound(edges, start, end, cost, tax, biases, N, debug = False):
    # For each edge there is flow * c(flow). These are the edgeFuncs. The global
    #   optimizer minimizes the sum of these functions

    initial =True

    preferences = {}
    edgeResults = {}

    # Add ids to every edge so that biases can be indexed
    for i, (n1, n2, edgeData) in enumerate(edges):
        edgeData['id'] = i

    G = networkx.MultiGraph()
    G.add_edges_from(edges)

    for i in range(N):
        for n1 in G.edge:
            for n2 in G.edge[n1]:
                for en in G.edge[n1][n2]:
                    preferences[(i, n1, n2, en)] = biases[G.edge[n1][n2][en]['id']](i)

    #zero the graph edges to start
    for n1 in G.edge:
        for n2 in G.edge[n1]:
            for en in G.edge[n1][n2]:
                G.edge[n1][n2][en]['f'] = 0.0

    # we need to preserve the balance of edges at the end of the round. becuas I should change my mind just because the flow changed...
    # If I change my mind, remove myself from the previous
    # for r in range(R):
    aCur = {} # create
    aPrev = None
    ct = 0
    history = []
    backtrack = False
    totalc = 0.0
    edgeResults = {}
    maxIters = 10
    while ((initial or aCur != aPrev) and ct < maxIters):
        ct += 1
        if aCur in history:
            backtrack=True
        history.append(dict(aCur))
        aPrev = dict(aCur)

        order = range(N)
        numpy.random.shuffle(order)
        for i in order:
            if i in aPrev:
                for n1, n2, betterEdgeIdx in aCur[i]:
                    G.edge[n1][n2][betterEdgeIdx]['f'] -= 1.0 / N

            for n1 in G.edge:
                for n2 in G.edge[n1]:
                    for en in G.edge[n1][n2]:
                        G.edge[n1][n2][en]['c'] = cost[G.edge[n1][n2][en]['t']](G.edge[n1][n2][en]['f']) + \
                                            tax[G.edge[n1][n2][en]['t']](G.edge[n1][n2][en]['f']) + \
                                            preferences[(i, n1, n2, en)]

            paths = networkx.all_simple_path(G, source = start, target = end)

            pathCosts = []

            for path in paths:
                c = 0
                edges = zip(path[:-1], path[1:])

                for n0, n1 in zip

            pEdge=list(zip(path[:-1], path[1:]))
            pEdge.sort()

            fullEdges = []
            for n1, n2 in pEdge: #loop over the path increasing flow
            # It's possible there are two paths from one node to another, we must choose the better one
                betterEdgeIdx, betterEdgeData = sorted(G.edge[n1][n2].items(), key = lambda x : x[1]['c'])[0]

                fullEdges.append((n1, n2, betterEdgeIdx))

            aCur[i] = fullEdges

            for n1, n2, betterEdgeIdx in aCur[i]:
                G.edge[n1][n2][betterEdgeIdx]['f'] += 1.0 / N

            totalc = 0.0
            edgeResults = {}
            for n1, n2 in set(G.edges()):
                for edgeIdx, edgeData in G.edge[n1][n2].items():
                    key = (n1, n2, edgeIdx)

                    edgeResults[key] = edgeData['f'], edgeData['t']
                    totalc += edgeData['f'] * cost[edgeData['t']](edgeData['f'])

            if debug:
                for (n1, n2, t), (f, t) in edgeResults.items():
                    print u"Edge ({0}, {1}), type {2}, flow {3}".format(n1, n2, t, f)

                print '----'
                print u"Total cost: {0}".format(numpy.mean(totalc))
                print '****'

        initial = False

        if debug:
            print 'Total iterations:', ct

    if debug:
        if backtrack:
            print "Game is not potential game"
        else:
            print "No backtracking detected"

    return totalc, edgeResults, backtrack, (ct < maxIters)

if __name__ == '__main__':
    #bias = lambda : 0
    #edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
    #     (0, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
    #     (1, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 1 }),
    #     (2, 3, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
    #     (1, 2, { 'f' : 0.0, 'c' : 0.0, 't' : 2 })]
    edges = [(0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 0 }),
             (0, 1, { 'f' : 0.0, 'c' : 0.0, 't' : 1 })]

    bias = [lambda i : 0, lambda i : 1.0]#numpy.random.exponential

    cost = [lambda x : x, lambda x : 1.00, lambda x : 0]
    tax = [lambda x : 0, lambda x : 0, lambda x : 0]

    start = 0
    end = 1

    N = 100 #number of players
    print runRound(edges, start, end, cost, tax, bias, N, True)