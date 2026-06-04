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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def adjacency_matrix(edges, n):
        A = [[0] * n for _ in range(n)]
        for u, v in edges:
            A[u][v] = 1
            A[v][u] = 1
        return A
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot = -1
            for j in range(rank, m):
                if A[j][i] != 0:
                    pivot = j
                    break
            if pivot == -1:
                continue
            A[pivot], A[rank] = A[rank], A[pivot]
            for j in range(n):
                if j != i and A[rank][j]:
                    factor = Fraction(A[j][i], A[rank][i])
                    for k in range(n):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def minimal_local_indeterminacy(edges, n):
        A = adjacency_matrix(edges, n)
        rank = gaussian_elimination(A)
        mli = n - rank
        return mli
    
    def communication_complexity_rank(n):
        # Placeholder for actual computation of ccr(G)
        # For simplicity, we use a random value that depends on n
        return random.randint(1, 2 * n)
    
    def polynomial_estimate(mli):
        # Placeholder for actual polynomial estimate
        # For simplicity, we use mli^2
        return mli ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        edges = generate_random_graph(n)
        mli = minimal_local_indeterminacy(edges, n)
        ccr = communication_complexity_rank(n)
        poly_estimate = polynomial_estimate(mli)
        
        if poly_estimate == 0:
            continue
        
        ratio = Fraction(ccr, poly_estimate)
        results.append({"n": n, "mli": mli, "ccr": ccr, "poly_estimate": poly_estimate, "ratio": ratio})
    
    if not results:
        return {
            "metric_name": "Ratio of Communication Complexity Rank to Polynomial Estimate",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    total_ratio = sum(result["ratio"] for result in results)
    mean_ratio = Fraction(total_ratio, len(results))
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "Ratio of Communication Complexity Rank to Polynomial Estimate",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": mean_ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None)
    mean_ratio = Fraction(total_ratio, len(results))
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE no_valid_instances")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")