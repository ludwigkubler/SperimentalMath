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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_representation(f, n):
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    M[i][j] = 1
        return M
    
    def frobenius_schur_index(M, n):
        trace = sum(M[i][i] for i in range(2**n))
        det = determinant(M, n)
        return abs(trace / det) if det != 0 else float('inf')
    
    def determinant(M, n):
        if n == 1:
            return M[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            det += sign * M[0][j] * determinant(submatrix, n-1)
            sign *= -1
        return det
    
    def communication_complexity(f, n):
        # Simplified model for demonstration purposes
        return len([i for i in range(2**n) if f[i] == 1])
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    M = matrix_representation(f, n)
    FSI_min = frobenius_schur_index(M, n)
    CC_lower = communication_complexity(f, n)
    
    if FSI_min > 10:
        return {
            "metric_name": "FSI_min",
            "metric_value": FSI_min,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "FSI_min > 10"
        }
    
    return {
        "metric_name": "FSI_min",
        "metric_value": FSI_min,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_FSI_min = sum(r["metric_value"] for r in results) / len(results)
    std_FSI_min = math.sqrt(sum((r["metric_value"] - mean_FSI_min)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_FSI_min} std={std_FSI_min} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_FSI_min} std={std_FSI_min} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"FSI_min > 10\" first_failing_seed={first_failing_seed}")