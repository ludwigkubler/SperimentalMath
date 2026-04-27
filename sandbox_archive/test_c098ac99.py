# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_random_3_regular_graph(n):
    while True:
        edges = set()
        vertices = list(range(n))
        random.shuffle(vertices)
        for i in range(n):
            j = (i + 1) % n
            k = (i + 2) % n
            if (vertices[i], vertices[j]) not in edges and (vertices[j], vertices[i]) not in edges:
                edges.add((vertices[i], vertices[j]))
            if (vertices[i], vertices[k]) not in edges and (vertices[k], vertices[i]) not in edges:
                edges.add((vertices[i], vertices[k]))
            if (vertices[j], vertices[k]) not in edges and (vertices[k], vertices[j]) not in edges:
                edges.add((vertices[j], vertices[k]))
        if len(edges) == n * 3 // 2:
            return [sorted(e) for e in edges]

def compute_laplacian(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    degree = [sum(1 for u, v in G if u == i or v == i) for i in range(n)]
    for i in range(n):
        L[i][i] = degree[i]
        for j in range(i + 1, n):
            if any((u, v) in G for u, v in [(i, j), (j, i)]):
                L[i][j] = -1
                L[j][i] = -1
    return L

def power_iteration(L, k=20):
    n = len(L)
    x = [random.random() for _ in range(n)]
    x /= math.sqrt(sum(x[i]**2 for i in range(n)))
    for _ in range(k):
        y = [sum(L[i][j] * x[j] for j in range(n)) for i in range(n)]
        y /= math.sqrt(sum(y[i]**2 for i in range(n)))
        x, y = y, x
    return x

def compute_lambda_2(L):
    n = len(L)
    v = power_iteration(L)
    lambda_1 = sum(v[i] * L[i][j] * v[j] for i in range(n) for j in range(i + 1, n))
    lambda_2 = -math.inf
    for _ in range(5):
        x = [random.random() for _ in range(n)]
        x -= sum(x[i] * v[i] for i in range(n)) * v
        x /= math.sqrt(sum(x[i]**2 for i in range(n)))
        lambda_2 = max(lambda_2, sum(x[i] * L[i][j] * x[j] for i in range(n) for j in range(i + 1, n)))
    return (lambda_1 + lambda_2) / 2

def compute_h(G):
    n = len(G)
    min_cut = float('inf')
    for s_size in range(1, n // 2 + 1):
        for s in itertools.combinations(range(n), s_size):
            cut_edges = sum(1 for u, v in G if (u in s and v not in s) or (v in s and u not in s))
            min_cut = min(min_cut, cut_edges / s_size)
    return min_cut

def compute_delta(G, lambda_2):
    beta_G = 2 * math.sqrt(3 * lambda_2)
    h_G = compute_h(G)
    return max(0, beta_G - h_G)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    for n in n_values:
        for _ in range(30):
            G = generate_random_3_regular_graph(n)
            c = {i: random.choice([0, 1]) for i in range(n)}
            lambda_2 = compute_lambda_2(compute_laplacian(G))
            delta_G = compute_delta(G, lambda_2)
            h_G = compute_h(G)
            L_G = h_G * (1 - delta_G / lambda_2) * n / 3 - 2
            w_T_G_c = float('inf')
            for k in range(n // 2 + 1):
                if all(all(c[u] != c[v] for u, v in G if u == i or v == i) for i in range(n)):
                    w_T_G_c = min(w_T_G_c, k)
            results.append((n, L_G, h_G * n / 2 + 2, w_T_G_c))
    metric_value = sum(max(0, L_G) <= w_T_G_c <= h_G_n_2_plus_2 for _, L_G, h_G_n_2_plus_2, w_T_G_c in results)
    instances_tested = len(results)
    conjecture_holds = metric_value >= 0.8 * instances_tested
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "w(T(G,c)) within bounds",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")