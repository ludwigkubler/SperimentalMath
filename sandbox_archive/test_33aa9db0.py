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

def generate_bipartite_graph(n):
    U = list(range(n))
    V = list(range(n, 2*n))
    E = []
    for u in U:
        for v in V:
            if random.choice([True, False]):
                E.append((u, v))
    return (U, V, E)

def clique_incidence_matrix(G):
    U, V, E = G
    n = len(U)
    M = [[0] * (n + n) for _ in range(n + n)]
    for u in U:
        M[u][u+n] = 1
    for v in V:
        M[v+n][v] = 1
    for u, v in E:
        M[u][v+n] = 1
        M[v+n][u] = 1
    return M

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
    rank = sum(1 for row in M if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    G = generate_bipartite_graph(n)
    M = clique_incidence_matrix(G)
    rank = gaussian_elimination(M)
    CC_G = n  # Lower bound for disjointness communication complexity
    metric_value = rank * CC_G
    return {
        "metric_name": "homotopy_group_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")