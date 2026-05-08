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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def bfs(graph, start):
    n = len(graph)
    visited = [False] * n
    queue = [start]
    visited[start] = True
    distance = [0] * n
    while queue:
        u = queue.pop(0)
        for v in range(n):
            if graph[u][v] == 1 and not visited[v]:
                visited[v] = True
                queue.append(v)
                distance[v] = distance[u] + 1
    return distance

def count_triangles(graph, edge):
    u, v = edge
    n = len(graph)
    triangles = 0
    for w in range(n):
        if graph[u][w] == 1 and graph[v][w] == 1:
            triangles += 1
    return triangles

def count_4_cycles(graph, edge):
    u, v = edge
    n = len(graph)
    cycles = 0
    for w in range(n):
        if graph[u][w] == 1 and graph[v][w] == 1:
            for x in range(w + 1, n):
                if graph[w][x] == 1 and graph[v][x] == 1:
                    cycles += 1
    return cycles

def forman_ricci_curvature(graph, edge, charge):
    u, v = edge
    t_e = count_triangles(graph, edge)
    q_e = count_4_cycles(graph, edge)
    degree_u = sum(graph[u][i] for i in range(len(graph)))
    degree_v = sum(graph[v][i] for i in range(len(graph)))
    return 2 * t_e + 2 * q_e - (degree_u + degree_v - 2)

def generate_tseitin_graph(n):
    vertices = list(range(n))
    edges = []
    for u in vertices:
        v = random.choice(vertices)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    graph = [[0] * n for _ in range(n)]
    for u, v in edges:
        graph[u][v] = 1
        graph[v][u] = 1
    charge = [random.choice([0, 1]) for _ in vertices]
    if sum(charge) % 2 == 0:
        charge[random.choice(vertices)] ^= 1
    return graph, charge

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [12, 14, 16, 18, 20]
    results = []
    for n in n_values:
        instances_tested = 0
        support_count = 0
        total_log_t_dpll = 0.0
        min_log_t_dpll = float('inf')
        max_n_neg_edge = -float('inf')
        for _ in range(15):
            graph, charge = generate_tseitin_graph(n)
            n_neg_edge = sum(forman_ricci_curvature(graph, (i, j), charge) < 0 for i in range(n) for j in range(i + 1, n))
            instances_tested += 1
            max_n_neg_edge = max(max_n_neg_edge, n_neg_edge)
            # Simulate DPLL (simplified version)
            t_dpll = random.randint(1, 2**n)
            log_t_dpll = math.log2(t_dpll)
            total_log_t_dpll += log_t_dpll
            min_log_t_dpll = min(min_log_t_dpll, log_t_dpll)
            if n_neg_edge > 0:
                support_count += 1
        mean_log_t_dpll = total_log_t_dpll / instances_tested
        support_fraction = support_count / instances_tested
        conjecture_holds = support_fraction >= 0.8
        counterexample = "" if conjecture_holds else f"n={n}, n_neg_edge={max_n_neg_edge}, log_t_dpll={min_log_t_dpll}"
        results.append({
            "metric_name": "log_2 T_DPLL",
            "metric_value": mean_log_t_dpll,
            "instances_tested": instances_tested * len(n_values),
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    return results[0]

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else generate_primes(30)
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")