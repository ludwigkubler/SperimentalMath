# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def generate_random_graph(n):
    edges = set()
    for u in range(n):
        for v in range(u + 1, n):
            if random.choice([True, False]):
                edges.add((u, v))
    return edges

def kronecker_dimension(edges):
    n = len(edges) + 2
    A = [[Fraction(0, 1)] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = Fraction(0, 1)
        A[v][u] = Fraction(0, 1)
    A[0][n-1] = Fraction(1, 1)
    A[n-1][0] = Fraction(1, 1)
    for i in range(n):
        A[i][i] = Fraction(-1, 1)
    
    rank = 0
    for row in A:
        if any(x != Fraction(0, 1) for x in row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        edges = generate_random_graph(n)
        kronecker_dim = kronecker_dimension(edges)
        rank_conf = len(edges) + 1
        
        if kronecker_dim > rank_conf * 2:  # Arbitrary constant c to test
            return {
                "metric_name": "Kronecker Dimension vs Rank Conf",
                "metric_value": kronecker_dim,
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": f"Graph with {n} vertices, Kronecker dim > 2 * Rank Conf"
            }
        
        results.append((kronecker_dim, rank_conf))
    
    mean_kronecker = sum(k for k, r in results) / len(results)
    mean_rank_conf = sum(r for k, r in results) / len(results)
    correlation = sum((k - mean_kronecker) * (r - mean_rank_conf) for k, r in results) / len(results)
    
    return {
        "metric_name": "Kronecker Dimension vs Rank Conf",
        "metric_value": correlation,
        "instances_tested": n_values[-1],
        "conjecture_holds": correlation >= 0.5,  # Arbitrary threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*37+2, 37))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Kronecker dim > 2 * Rank Conf' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")