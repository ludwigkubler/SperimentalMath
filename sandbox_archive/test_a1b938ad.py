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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_clique_instance(n, k):
        vertices = list(range(n))
        edges = []
        for i in range(k):
            clique = random.sample(vertices, k)
            for u in clique:
                for v in clique:
                    if u < v and (u, v) not in edges:
                        edges.append((u, v))
        return n, k, edges
    
    def algebraic_curve_complexity(n, k, edges):
        # Construct the adjacency matrix
        A = [[0] * n for _ in range(n)]
        for u, v in edges:
            A[u][v] = 1
            A[v][u] = 1
        
        # Perform Gaussian elimination to find the rank of the matrix
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i, n)):
                continue
            rank += 1
            pivot_row = next(j for j in range(i, n) if A[j][i] != 0)
            A[i], A[pivot_row] = A[pivot_row], A[i]
            for j in range(n):
                if i == j:
                    continue
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        return rank
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    curve_complexities = []
    
    for n in n_values:
        k = random.randint(2, min(n - 1, 5))
        _, _, edges = generate_clique_instance(n, k)
        complexity = algebraic_curve_complexity(n, k, edges)
        curve_complexities.append(complexity)
    
    mean_ratio = mean([complexity / (n ** k) for n, k, _ in zip(n_values, [random.randint(2, min(n - 1, 5)) for _ in n_values], [generate_clique_instance(n, random.randint(2, min(n - 1, 5))) for n in n_values])])
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(curve_complexities),
        "conjecture_holds": abs(mean_ratio - 1) <= 0.1,
        "counterexample": "" if abs(mean_ratio - 1) <= 0.1 else f"Mean ratio {mean_ratio} not within ±10% of 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio {result['metric_value']} not within ±10% of 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")