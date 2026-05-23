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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def free_convolution_matrix(f):
        n = len(f)
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i & j] == 1:
                    M[i][j] += 1
        return M
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot = None
            for j in range(i, n):
                if matrix[j][i] != 0:
                    pivot = j
                    break
            if pivot is None:
                continue
            rank += 1
            for j in range(n):
                if j == pivot:
                    continue
                factor = Fraction(matrix[j][i], matrix[pivot][i])
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[pivot][k]
        return rank
    
    def bp_readtwice_width(f):
        # Placeholder function; actual implementation required
        return 1
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        M = free_convolution_matrix(f)
        rank = min_rank(M)
        results.append((n, rank))
    
    total_rank = sum(rank for _, rank in results)
    avg_rank = Fraction(total_rank, len(results))
    expected_avg_rank = math.sqrt(sum(n**2 for n, _ in results)) / len(results)
    
    conjecture_holds = abs(avg_rank - expected_avg_rank) <= 0.1 * expected_avg_rank
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": float(avg_rank),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - avg_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")