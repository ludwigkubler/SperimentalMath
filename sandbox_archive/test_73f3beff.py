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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            for k in range(i + 1, n):
                factor = A[k][i] / A[i][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
        
        return A
    
    def r_transform(A):
        n = len(A)
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    B[i][j] = 1
                else:
                    B[i][j] = A[i][j]
        
        det_A = 1
        for i in range(n):
            det_A *= A[i][i]
        
        return sum(sum(B[i][j] * det_A / (math.factorial(i) * math.factorial(j)) for j in range(n)) for i in range(n))

    def is_inner_product_mod_2(A):
        n = len(A)
        for i in range(n):
            for j in range(n):
                if A[i][j] % 2 != 0:
                    return False
        return True

    def free_entropy(P):
        return r_transform(P)

    m = random.randint(5, 40)
    P = [[random.choice([-1, 1]) for _ in range(m)] for _ in range(m)]
    P = gaussian_elimination(P)
    
    if is_inner_product_mod_2(P):
        rho_P = free_entropy(P)
        return {
            "metric_name": "free_entropy",
            "metric_value": rho_P,
            "instances_tested": 1,
            "conjecture_holds": rho_P <= 10 * math.log(m),
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "free_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = supported_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")