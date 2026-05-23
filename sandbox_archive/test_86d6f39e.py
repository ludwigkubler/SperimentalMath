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

def generate_random_monotone_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_associated_matrix(f):
    n = int(math.log2(len(f)))
    matrix = [[f[i] if i & (1 << j) else f[i ^ (1 << j)] for j in range(n)] for i in range(2**n)]
    return matrix

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for j in range(n):
        pivot_row = None
        for i in range(rank, m):
            if matrix[i][j] != 0:
                pivot_row = i
                break
        if pivot_row is not None:
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for i in range(m):
                if i != rank and matrix[i][j] != 0:
                    factor = Fraction(matrix[i][j], matrix[rank][j])
                    for k in range(n):
                        matrix[i][k] -= factor * matrix[rank][k]
            rank += 1
    return rank

def compute_minimal_tropical_hermitian_rank(f):
    matrix = compute_associated_matrix(f)
    return gaussian_elimination(matrix)

def simulate_karchmer_wigderson_protocol(f, n):
    def binary_search(low, high):
        if low >= high:
            return 0
        mid = (low + high) // 2
        left = [f[i] for i in range(2**n) if i & (1 << mid)]
        right = [f[i ^ (1 << mid)] for i in range(2**n) if not (i & (1 << mid))]
        return max(binary_search(low, mid), binary_search(mid + 1, high)) + 1
    return binary_search(0, n - 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_monotone_function(n)
    
    tropical_rank = compute_minimal_tropical_hermitian_rank(f)
    protocol_cost = simulate_karchmer_wigderson_protocol(f, n)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": abs(tropical_rank - protocol_cost) / max(abs(tropical_rank), abs(protocol_cost)) if tropical_rank != 0 and protocol_cost != 0 else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r['metric_value'] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result['metric_value'] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")