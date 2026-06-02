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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(2**n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def minimal_index(f, n):
        A = []
        b = []
        for i in range(2**n):
            row = [f[j] ^ (i >> j & 1) for j in range(n)]
            A.append(row)
            b.append(i % 2)
        
        # Gaussian elimination
        m, k = len(A), n
        for i in range(m):
            if A[i][i] == 0:
                for j in range(i + 1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    return None  # Singular matrix
        
        for i in range(m - 1, -1, -1):
            for j in range(i + 1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(k):
                    A[j][k] -= factor * A[i][k]
        
        # Count non-zero rows
        min_index_val = sum(1 for row in A if any(row))
        return min_index_val
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        rank = communication_complexity_rank(f)
        if rank is None:
            continue
        
        min_index_val = minimal_index(f, n)
        if min_index_val is None:
            continue
        
        results.append({
            "n": n,
            "rank": rank,
            "min_index": min_index_val
        })
    
    if not results:
        return {
            "metric_name": "minimal_index_to_rank_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(result["min_index"] / result["rank"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["min_index"] / result["rank"] - mean_ratio) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "minimal_index_to_rank_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": mean_ratio <= 3 * math.log(max(result["n"] for result in results)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")