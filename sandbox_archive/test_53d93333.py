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

def generate_k_clique(n, k):
    if n < k:
        return None
    vertices = list(range(n))
    edges = []
    for i in range(k):
        for j in range(i + 1, k):
            edges.append((vertices[i], vertices[j]))
    return edges

def monomial_to_index(monomial, n):
    index = 0
    for vertex in monomial:
        index |= (1 << vertex)
    return index

def ideal_to_matrix(n, edges):
    matrix = [[0] * (2**n) for _ in range(2**n)]
    for edge in edges:
        i = monomial_to_index(edge, n)
        j = monomial_to_index((edge[1], edge[0]), n)
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if matrix[i][rank]:
            for j in range(i + 1, n):
                if matrix[j][rank]:
                    pivot_row = matrix[j]
                    current_row = matrix[i]
                    for k in range(n):
                        pivot_row[k] ^= current_row[k]
            rank += 1
    return rank

def minimal_rank(n, k):
    edges = generate_k_clique(n, k)
    if not edges:
        return None
    matrix = ideal_to_matrix(n, edges)
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            k = random.randint(2, min(n - 1, 3))
            rank = minimal_rank(n, k)
            if rank is None:
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": float('inf'),
                    "instances_tested": len(results),
                    "conjecture_holds": False,
                    "counterexample": "k_clique_not_possible"
                }
            results.append(rank)
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    conjecture_holds = all(x <= n ** (1.5 - k) for rank, n, k in zip(results, n_values, [random.randint(2, min(n - 1, 3)) for _ in range(len(results))]))
    counterexample = "None" if conjecture_holds else "k_clique_not_possible"
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"k_clique_not_possible\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")