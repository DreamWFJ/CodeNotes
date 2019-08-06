# -*- coding: utf-8 -*-
# USER: Test
# Time: 2019/7/29 10:51

from collections import deque


def recursive_dfs(g, s, result=None):
    if result is None:
        result = set()
    result.add(s)
    for u in g[s]:
        if u in result:
            continue
        recursive_dfs(g, u, result)


def iter_dfs(g, s):
    result, queue = set(), list()
    queue.append(s)
    while queue:
        u = queue.pop()
        if u in result:
            continue
        result.add(u)
        queue.extend(g[u])
        yield u


def dfs_topsort(g):
    s, res = set(), list()

    def recursive(u):
        if u in s:
            return
        s.add(u)
        for v in g[u]:
            recursive(v)
        res.append(u)

    for u in g:
        recursive(u)
    res.reverse()
    return res


def bfs(g, s):
    p, q = {s: None}, deque([s])
    while q:
        u = q.popleft()
        for v in g[u]:
            if v in p:
                continue
            p[v] = u
            q.append(v)
    return p
