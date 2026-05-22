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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def indicator_vector(f, n):
        return [[f[i] if j == i else 0 for j in range(2**n)] for i in range(2**n)]
    
    def matroid_rank(indicator_vectors):
        n = len(indicator_vectors)
        A = []
        for v in indicator_vectors:
            A.append([v[j] for j in range(n)])
        
        rank = 0
        for i in range(n):
            if any(all(A[k][j] == 0 for j in range(i)) for k in range(rank)):
                continue
            rank += 1
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(m):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(m):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def matroid_rank_gaussian(indicator_vectors):
        n = len(indicator_vectors)
        A = gaussian_elimination(indicator_vectors)
        rank = sum(1 for row in A if any(row[j] != 0 for j in range(n)))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        ind_vectors = indicator_vector(f, n)
        rank = matroid_rank(ind_vectors)
        results.append((n, rank))
    
    mean_rank = sum(rank for _, rank in results) / len(results)
    std_dev = math.sqrt(sum((rank - mean_rank)**2 for _, rank in results) / len(results))
    conjecture_holds = all(rank >= n * math.log(n) for n, rank in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")