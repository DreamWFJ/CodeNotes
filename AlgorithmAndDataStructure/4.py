# -*- coding: utf-8 -*-
# USER: Test
# Time: 2019/7/29 15:17

inf = float('inf')


def relax(W, u, v, D, P):
    """
    松弛算法
    :param W:
    :param u:
    :param v:
    :param D:
    :param P:
    :return:
    """
    d = D.get(u, inf) + W[u][v]
    if d < D.get(v, inf):
        D[v], P[v] = d, u
        return True
    return False


def bellman_ford(G, s):
    D, P = {s: 0}, dict()
    for rnd in G:
        changed = False
        for u in G:
            for v in G[u]:
                changed = relax(G, u, v, D, P)
        if not changed:
            break
    else:
        raise ValueError
    return D, P
