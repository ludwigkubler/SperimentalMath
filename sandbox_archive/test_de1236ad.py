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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def boolean_function_to_matrix(f, n):
    matrix = []
    for i in range(2**n):
        row = [f[i >> j & 1] for j in range(n)]
        matrix.append(row)
    return matrix

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(n):
        max_row = rank
        for j in range(rank, m):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        if matrix[max_row][i] == 0:
            continue
        matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
        for j in range(m):
            if i != j:
                factor = -matrix[j][i] / matrix[rank][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def entropic_complexity(f, n):
    counts = [0] * (2**n)
    for i in range(2**n):
        counts[f[i]] += 1
    entropy = 0.0
    for count in counts:
        if count > 0:
            prob = count / (2**n)
            entropy -= prob * math.log2(prob)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        matrix = boolean_function_to_matrix(f, n)
        rank_quot = gaussian_elimination(matrix)
        entropy_complexity_val = entropic_complexity(f, n)
        
        if rank_quot == 0 or entropy_complexity_val == 0:
            continue
        
        results.append((rank_quot / entropy_complexity_val))
    
    if not results:
        return {
            "metric_name": "Rank_quot / Entropy_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    
    return {
        "metric_name": "Rank_quot / Entropy_complexity",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": all(x <= 10 for x in results),  # Arbitrary upper bound
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std={math.sqrt(sum((r['metric_value'] - (sum(r['metric_value'] for r in results) / len(results)))**2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")