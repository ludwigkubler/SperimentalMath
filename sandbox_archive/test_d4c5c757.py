# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def is_subset(a, b):
    return all(x in b for x in a)

def is_antichain(antichain):
    for a, b in itertools.combinations(antichain, 2):
        if is_subset(a, b) or is_subset(b, a):
            return False
    return True

def generate_random_antichain(n, k):
    antichain = []
    for _ in range(k):
        while True:
            candidate = frozenset(random.sample(range(n), random.randint(1, n)))
            if all(not is_subset(candidate, a) and not is_subset(a, candidate) for a in antichain):
                antichain.append(candidate)
                break
    return antichain

def compute_minterms_and_maxterms(f):
    minterms = []
    maxterms = []
    for x in itertools.product([0, 1], repeat=len(f)):
        if f(x):
            minterms.append(frozenset(i for i, v in enumerate(x) if v == 1))
        else:
            maxterms.append(frozenset(i for i, v in enumerate(x) if v == 1))
    return minterms, maxterms

def build_bipartite_graph(minterms, maxterms):
    graph = {}
    for m in minterms:
        for k in maxterms:
            edge = (m, k)
            multiplicity = len(m & k)
            if edge in graph:
                graph[edge] += multiplicity
            else:
                graph[edge] = multiplicity
    return graph

def compute_laplacian(graph, vertices):
    n = len(vertices)
    laplacian = [[0] * n for _ in range(n)]
    for i, u in enumerate(vertices):
        for j, v in enumerate(vertices):
            if i == j:
                degree = sum(graph.get((u, v), 0) for v in vertices if u != v)
                laplacian[i][j] = degree
            else:
                laplacian[i][j] = -graph.get((u, v), 0)
    return laplacian

def matrix_determinant(matrix):
    n = len(matrix)
    det = 1
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    det *= -1
                    break
            else:
                return 0
        det *= matrix[i][i]
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
    return det

def compute_spanning_trees(laplacian):
    n = len(laplacian)
    if n == 0:
        return 0
    reduced_laplacian = [row[1:] for row in laplacian[1:]]
    det = matrix_determinant(reduced_laplacian)
    return det

def compute_sigma(minterms, maxterms, graph):
    vertices = list(minterms) + list(maxterms) + ['g']
    laplacian = compute_laplacian(graph, vertices)
    tau = compute_spanning_trees(laplacian)
    if tau <= 0:
        return 0
    return math.log2(1 + tau)

def compute_dkw(f, minterms, maxterms):
    if len(minterms) == 0 or len(maxterms) == 0:
        return 0
    dkw = float('inf')
    for m in minterms:
        for k in maxterms:
            if not is_subset(m, k):
                dkw = min(dkw, len(m) + len(k))
    return dkw

def run_trial(seed):
    random.seed(seed)
    n = random.choice([4, 5, 6, 7, 8])
    k = random.randint(2, 6)
    antichain = generate_random_antichain(n, k)
    f = lambda x: any(is_subset(a, x) for a in antichain)
    minterms, maxterms = compute_minterms_and_maxterms(f)
    graph = build_bipartite_graph(minterms, maxterms)
    sigma = compute_sigma(minterms, maxterms, graph)
    dkw = compute_dkw(f, minterms, maxterms)
    bound = dkw * (len(minterms) + len(maxterms) + 1) * math.log2(n + 2)
    conjecture_holds = sigma <= bound
    counterexample = "" if conjecture_holds else f"sigma={sigma} > bound={bound} for n={n}, k={k}"
    return {
        "metric_name": "sigma_bound_ratio",
        "metric_value": sigma / bound if bound != 0 else 0,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def main():
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break

if __name__ == "__main__":
    main()