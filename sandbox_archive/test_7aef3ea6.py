# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def gaussian_elimination(A, B):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        B[i], B[max_row] = B[max_row], B[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            B[j] -= factor * B[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (B[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += (-1) ** i * A[0][i] * determinant(submatrix)
    return det

def inverse(A):
    n = len(A)
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is singular")
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = (-1) ** (i+j) * determinant(submatrix)
            adjugate[j][i] = cofactor
    return matrix_multiply(adjugate, Fraction(1, det))

def random_3_regular_graph(n):
    if n % 2 != 0:
        return None
    edges = set()
    while len(edges) < n * (n - 1) // 6:
        u, v = random.sample(range(n), 2)
        if u == v or (u, v) in edges or (v, u) in edges:
            continue
        edges.add((u, v))
        edges.add((v, u))
    return list(edges)

def is_connected(graph):
    n = len(graph)
    visited = [False] * n
    stack = [0]
    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = True
            for v in range(n):
                if (u, v) in graph or (v, u) in graph and not visited[v]:
                    stack.append(v)
    return all(visited)

def spectral_gap(graph):
    n = len(graph)
    A = [[0] * n for _ in range(n)]
    d = [sum(1 for v in range(n) if (u, v) in graph or (v, u) in graph) for u in range(n)]
    for u in range(n):
        for v in range(n):
            if (u, v) in graph or (v, u) in graph:
                A[u][v] = -1 / d[v]
            elif u == v:
                A[u][v] = 1 + sum(1 / d[i] for i in range(n) if i != u)
    L = matrix_multiply(inverse(A), A)
    eigenvalues = [0] * n
    for _ in range(100):
        x = [random.random() for _ in range(n)]
        x /= sum(x)
        x_new = matrix_multiply(L, x)
        x_new /= sum(x_new)
        eigenvalue = sum(x[i] * x_new[i] for i in range(n))
        if abs(eigenvalue - eigenvalues[-1]) < 1e-6:
            break
        eigenvalues.append(eigenvalue)
    return max(eigenvalues) - min(eigenvalues)

def random_01_charge(n):
    c = [random.choice([0, 1]) for _ in range(n)]
    if sum(c) % 2 == 0:
        c[random.randint(0, n-1)] ^= 1
    return c

def dhar_burning(graph, charge, sink):
    n = len(graph)
    q_reduced = charge[:]
    queue = [sink]
    while queue:
        u = queue.pop()
        for v in range(n):
            if (u, v) in graph or (v, u) in graph and q_reduced[v] > 0:
                q_reduced[v] -= 1
                if q_reduced[v] == 0:
                    queue.append(v)
    return q_reduced

def baker_norine_rank(graph, charge):
    n = len(graph)
    sink = random.randint(0, n-1)
    q_reduced = dhar_burning(graph, charge, sink)
    rank = sum(q_reduced[v] > 0 for v in range(n))
    return rank

def tseitin_cnf(graph, charge):
    n = len(graph)
    cnf = []
    for u in range(n):
        if charge[u]:
            cnf.append([u+1])
        else:
            cnf.append([-u-1])
    for u in range(n):
        for v in range(u+1, n):
            if (u, v) in graph or (v, u) in graph:
                cnf.append([-u-1, -v-1])
                cnf.append([u+1, v+1])
    return cnf

def dpll(cnf):
    stack = []
    assignment = [None] * len(cnf)
    def backtrack():
        if not stack:
            return True
        literal = stack.pop()
        var = abs(literal) - 1
        sign = literal > 0
        assignment[var] = sign
        for clause in cnf:
            if literal in clause:
                clause.remove(literal)
            elif -literal in clause:
                clause.remove(-literal)
                if not clause:
                    return False
        if backtrack():
            return True
        assignment[var] = None
        stack.append(-literal)
        for clause in cnf:
            if -literal in clause:
                clause.remove(-literal)
                if literal in clause:
                    clause.remove(literal)
                    if not clause:
                        return False
        if backtrack():
            return True
    stack.extend([i+1 for i in range(len(cnf))])
    return backtrack()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 10, 12, 14]:
        graph = random_3_regular_graph(n)
        while not graph or not is_connected(graph) or spectral_gap(graph) < 0.15:
            graph = random_3_regular_graph(n)
        charge = random_01_charge(n)
        rank = baker_norine_rank(graph, charge)
        g = n - rank
        cnf = tseitin_cnf(graph, charge)
        leaf_count = 0
        max_width = 0
        for _ in range(30):
            if not dpll(cnf):
                leaf_count += 1
                width = max(len(clause) for clause in cnf)
                if width > max_width:
                    max_width = width
        results.append((g, leaf_count, max_width))
    total_leaf_count = sum(count for _, count, _ in results)
    total_max_width = sum(width for _, _, width in results)
    mean_log2_leaf_count_per_g = sum(Fraction(log2(count), g) for g, count, _ in results) / len(results)
    mean_max_width_per_g = sum(Fraction(width, g) for g, _, width in results) / len(results)
    support_fraction = all(0.5 <= log2(count) / g <= 1.5 and 0.5 <= width / g <= 3 for g, count, width in results)
    return {
        "metric_name": "D(G,c)",
        "metric_value": mean_log2_leaf_count_per_g,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r >= 0.5 and r <= 1.5) / len(results)
    print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")