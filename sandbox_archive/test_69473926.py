# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_graph(n):
    if n == 1:
        return {0: set()}
    edges = []
    for i in range(1, n):
        u = random.choice(range(i))
        v = i
        edges.append((u, v))
    graph = {i: set() for i in range(n)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph

def is_connected(graph):
    visited = [False] * len(graph)
    stack = [0]
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            stack.extend(graph[node])
    return all(visited)

def find_cycle(graph, start, path=[]):
    path = path + [start]
    if start in graph[start]:  # Cycle of length 3 or more
        return path
    for node in graph[start]:
        if node not in path:
            newpath = find_cycle(graph, node, path)
            if newpath: return newpath
    return None

def is_cyclic(graph):
    return any(find_cycle(graph, node) for node in range(len(graph)))

def automorphism_group_order(matroid):
    n = len(matroid)
    adj_matrix = [[0] * n for _ in range(n)]
    for u, v in matroid:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1

    def is_permutation(p):
        return all(len(set(p)) == len(p) and sorted(p) == list(range(n)) for p in p)

    def is_isomorphic(graph1, graph2):
        if len(graph1) != len(graph2):
            return False
        for perm in itertools.permutations(range(n)):
            if is_permutation(perm):
                permuted_graph = {perm[u]: {perm[v] for v in graph2[u]} for u in range(n)}
                if permuted_graph == graph2:
                    return True
        return False

    automorphisms = [tuple(range(n))]
    for p in itertools.permutations(range(n)):
        if is_permutation(p):
            permuted_adj_matrix = [[adj_matrix[p[i]][p[j]] for j in range(n)] for i in range(n)]
            if is_isomorphic(adj_matrix, permuted_adj_matrix):
                automorphisms.append(tuple(p))

    return len(automorphisms)

def resolution_proof_width(matroid):
    n = len(matroid)
    clauses = []
    for u, v in matroid:
        clause = [-u-1, -v-1]
        clauses.append(clause)

    def is_tautology(clauses):
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_satisfiable(clauses):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable(clauses):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]
                new_clauses = []
                for c in clauses:
                    if literal in c:
                        continue
                    if -literal in c:
                        new_clauses.append([x for x in c if x != -literal])
                    else:
                        new_clauses.append(c)
                clauses = new_clauses
            else:
                stack.append(clause)
        return False

    def is_resolvable_with_width(width):
        visited = [False] * n
        stack = []
        while clauses:
            clause = clauses.pop()
            if not clause:
                return True
            unit_clause = [x for x in clause if x < 0]
            if unit_clause:
                literal = -unit_clause[0]