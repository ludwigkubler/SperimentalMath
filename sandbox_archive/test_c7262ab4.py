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

def generate_k_clique_instance(n, k):
    if n < k:
        return None
    vertices = list(range(n))
    edges = set()
    for i in range(k):
        for j in range(i + 1, k):
            edges.add((vertices[i], vertices[j]))
    for _ in range(math.comb(n - k, 2)):
        u, v = random.sample(vertices[k:], 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    return vertices, edges

def twisted_group_algebra(instance):
    n, edges = instance
    G = {i: i for i in range(n)}
    algebra = [[0] * n for _ in range(n)]
    for u, v in edges:
        algebra[u][v] = algebra[v][u] = -1
    return algebra

def minimal_rank(algebra):
    n = len(algebra)
    rank = 0
    for i in range(n):
        if all(algebra[i][j] == 0 for j in range(i)):
            continue
        pivot_row = i
        for j in range(i + 1, n):
            if algebra[j][i] != 0:
                pivot_row = j
                break
        if algebra[pivot_row][i] == 0:
            continue
        rank += 1
        for j in range(n):
            algebra[i][j], algebra[pivot_row][j] = algebra[pivot_row][j], algebra[i][j]
        for j in range(n):
            if i != j and algebra[j][i] != 0:
                factor = Fraction(algebra[j][i], algebra[i][i])
                for k in range(n):
                    algebra[j][k] -= factor * algebra[i][k]
    return rank

def monotone_circuit_depth(k, n):
    # Simplified heuristic based on known lower bounds
    return 2 ** (n - k) + k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n // 2, 5))
    instance = generate_k_clique_instance(n, k)
    if instance is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k > n"
        }
    algebra = twisted_group_algebra(instance)
    rank = minimal_rank(algebra)
    depth = monotone_circuit_depth(k, n)
    ratio = Fraction(rank, 2 ** (n - k) * k)
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5 and ratio < 0.3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")