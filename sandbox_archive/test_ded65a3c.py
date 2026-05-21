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

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))

def union_find(n):
    parent = list(range(n))
    rank = [0] * n

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            elif rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            else:
                parent[root_j] = root_i
                rank[root_i] += 1

    return union, find

def mst_edge_weights(M):
    n = len(M)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            weight = hamming_distance(M[i], M[j])
            if weight > 0:
                edges.append((weight, (i, j)))
    
    union, find = union_find(n)
    mst_edges = []
    edges.sort()
    for weight, (i, j) in edges:
        if find(i) != find(j):
            union(i, j)
            mst_edges.append(weight)
    
    return mst_edges

def persistence_entropy(weights):
    if not weights:
        return 0
    total_weight = sum(weights)
    freqs = [weight / total_weight for weight in weights]
    pe = -sum(freq * math.log2(freq) for freq in freqs)
    return pe

def rank_real(M, tol=1e-8):
    u, s, vh = zip(*M)
    rank = sum(1 for x in s if abs(x) > tol)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 16, 24, 32]
    results = []
    
    for n in n_values:
        for _ in range(5):
            if n == 8:
                M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
            elif n == 16:
                r = random.randint(1, 2)
                A = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
                B = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
                M = [[int(math.copysign(1, a[i] * b[j])) for j in range(n)] for i in range(n)]
            elif n == 24:
                r = random.randint(4, 8)
                A = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
                B = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
                M = [[int(math.copysign(1, a[i] * b[j])) for j in range(n)] for i in range(n)]
            elif n == 32:
                r = random.randint(4, 8)
                A = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
                B = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
                M = [[int(math.copysign(1, a[i] * b[j])) for j in range(n)] for i in range(n)]
            else:
                return {"metric_name": "PE", "metric_value": None, "instances_tested": 0, "conjecture_holds": False, "counterexample": "mapping_undefined"}
            
            weights = mst_edge_weights(M)
            pe = persistence_entropy(weights)
            rank = rank_real(M)
            if 2 ** pe > rank + 1:
                results.append((n, pe, rank, True))
            else:
                results.append((n, pe, rank, False))
    
    metric_value = sum(pe for n, pe, rank, _ in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(not holds for _, _, _, holds in results)
    counterexample = "None" if conjecture_holds else f"n={n}, PE={pe}, rank={rank}"
    
    return {
        "metric_name": "PE",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"None\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")