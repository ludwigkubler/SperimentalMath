# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_graph(n):
    graph = [[0] * n for _ in range(n)]
    edges = list(combinations(range(n), 2))
    num_edges = len(edges)
    for i in range(num_edges):
        u, v = edges[i]
        if random.random() < 0.5:
            graph[u][v] = graph[v][u] = 1
    return graph

def max_cut_polynomial(graph):
    n = len(graph)
    poly = 0
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                poly += f"x{i} * x{j}"
    return poly

def degree_d_monomials(n, d):
    monomials = set()
    variables = list(range(n))
    def generate_monomial(monomial, depth):
        if depth == d:
            monomials.add('*'.join(sorted(monomial)))
            return
        for var in variables:
            if var not in monomial:
                generate_monomial(monomial + (var,), depth + 1)
    generate_monomial((), 0)
    return sorted(monomials)

def gram_matrix(monomials, graph):
    n = len(graph)
    m = len(monomials)
    G = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i, m):
            monomial_i = monomials[i].split('*')
            monomial_j = monomials[j].split('*')
            count = 0
            for var in set(monomial_i + monomial_j):
                if var in monomial_i and var in monomial_j:
                    count += graph[int(var)][int(var)]
            G[i][j] = count
            G[j][i] = count
    return G

def matrix_rank(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if any(matrix[j][i] != 0 for j in range(rank)):
            for j in range(i, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            for j in range(n):
                if i != j:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    graph = generate_random_graph(n)
    d = math.floor(math.log(n) / math.log(math.log(n)))
    poly = max_cut_polynomial(graph)
    monomials = degree_d_monomials(n, d)
    G = gram_matrix(monomials, graph)
    rank = matrix_rank(G)
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= 0.1 * n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or mapping undefined")