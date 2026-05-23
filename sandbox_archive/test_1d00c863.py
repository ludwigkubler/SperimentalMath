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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                if i == k:
                    A[j][k] = 0
                else:
                    A[j][k] += factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def generate_k_clique_instance(n, k):
    edges = set()
    while len(edges) < k:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    return edges

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        while len(results) < 30:  # Ensure at least 30 instances per seed
            edges = generate_k_clique_instance(n, k)
            if not edges:
                continue
            
            # Construct the matrix A from the clique instance
            A = [[0] * n for _ in range(n)]
            for u, v in edges:
                A[u][v] = 1
                A[v][u] = 1
            
            rank = gaussian_elimination(A)
            total_rank += rank
            instances_tested += 1
        
        if instances_tested == 0:
            continue
        
        ratio = Fraction(total_rank, n * instances_tested)
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "rank_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= Fraction(n, n**0.25)) / len(results)
    
    return {
        "metric_name": "rank_ratio",
        "metric_value": float(mean),
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"first_failing_seed={seed}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(r is not None for r in results):
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r >= Fraction(n, n**0.25)) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[next(i for i, r in enumerate(results) if r < Fraction(n, n**0.25))]
            print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some results are None")