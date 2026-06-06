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
    
    def function_to_matrix(f, n):
        M = []
        for i in range(2**n):
            binary = format(i, f'0{n}b')
            row = [f(int(binary[j])) for j in range(n)]
            M.append(row)
        return M
    
    def matrix_rank(M):
        m, n = len(M), len(M[0])
        if m == 0 or n == 0:
            return 0
        rank = min(m, n)
        indices = list(range(min(m, n)))
        for i in range(rank):
            pivot = max(abs(M[j][indices[i]]) for j in range(i, m))
            if pivot == 0:
                rank -= 1
                indices[i:] = indices[i+1:]
                continue
            for j in range(i, m):
                M[j][i] /= pivot
            for j in range(m):
                if j != i:
                    factor = M[j][i]
                    for k in range(n):
                        M[j][k] -= factor * M[i][k]
        return rank
    
    def frobenius_schur_indicator(M):
        m, n = len(M), len(M[0])
        if m != n:
            raise ValueError("Matrix must be square")
        trace = sum(M[i][i] for i in range(m))
        det = 1
        for i in range(m):
            det *= M[i][i]
        return Fraction(trace**2, det)
    
    def generate_random_function(n):
        return lambda x: random.choice([0, 1])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_random_function(n)
        M = function_to_matrix(f, n)
        rank = matrix_rank(M)
        indicator = frobenius_schur_indicator(M)
        results.append((n, rank, indicator))
    
    var_rank = sum((rank - sum(rank for _, rank, _ in results) / len(results))**2 for _, rank, _ in results) / len(results)
    conjecture_holds = all(var_rank <= indicator for _, _, indicator in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "variance_of_rank",
        "metric_value": var_rank,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_var_rank = sum(r["metric_value"] for r in results) / len(results)
    std_var_rank = math.sqrt(sum((r["metric_value"] - mean_var_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_var_rank} std={std_var_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")