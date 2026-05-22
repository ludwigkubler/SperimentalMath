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
    
    def matroid_rank(f):
        n = len(f)
        indicator_vectors = [[int(x[i] == j) for i in range(n)] for j in range(2)]
        rank = 0
        while True:
            found_new_vector = False
            new_vector = [random.randint(0, 1) for _ in range(n)]
            if all(sum(v * iv[j] for v, iv in zip(new_vector, indicator_vectors)) == 0 for j in range(len(indicator_vectors))):
                indicator_vectors.append(new_vector)
                rank += 1
                found_new_vector = True
            if not found_new_vector:
                break
        return rank
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_rank(A):
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        M_f_rank = matroid_rank(f)
        A = [[int(x[i] == j) for i in range(n)] for j in range(2)]
        M_A_rank = matrix_rank(A)
        
        results.append({
            "n": n,
            "f": f,
            "M_f_rank": M_f_rank,
            "A": A,
            "M_A_rank": M_A_rank
        })
    
    total_rank = sum(result["M_f_rank"] for result in results)
    mean_rank = total_rank / len(results)
    std_deviation = math.sqrt(sum((result["M_f_rank"] - mean_rank) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["M_f_rank"] >= n * math.log(n, 2) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank of Matroid",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")