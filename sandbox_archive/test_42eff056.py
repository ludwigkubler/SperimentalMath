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
    
    def matrix_representation(f):
        n = int(math.log2(len(f)))
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[i*2 + (j >> 1)] != f[j*2 + (i >> 1)]:
                    M[i][j] = 1
        return M
    
    def frobenius_schur_index(M):
        n = len(M)
        trace = sum(M[i][i] for i in range(n))
        det = determinant(M, n)
        if det == 0:
            return float('inf')
        return abs(trace / det)
    
    def determinant(M, n):
        if n == 1:
            return M[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            det += (-1)**j * M[0][j] * determinant(submatrix, n-1)
        return det
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_comm = 0
        for i in range(2**n):
            comm = sum(1 for j in range(n) if f[i ^ (1 << j)] != f[i])
            if comm > max_comm:
                max_comm = comm
        return max_comm
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_fsi_min = 0.0
    total_cc_lower = 0.0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            M = matrix_representation(f)
            FSI_min = frobenius_schur_index(M)
            CC_lower = communication_complexity(f)
            
            if FSI_min > 10:
                return {
                    "metric_name": "FSI_min",
                    "metric_value": FSI_min,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": "FSI_min > 10"
                }
            
            total_fsi_min += FSI_min
            total_cc_lower += CC_lower
            instances_tested += 1
    
    mean_fsi_min = total_fsi_min / instances_tested
    mean_cc_lower = total_cc_lower / instances_tested
    
    return {
        "metric_name": "FSI_min",
        "metric_value": mean_fsi_min,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": mean_fsi_min >= 0.8 * mean_cc_lower,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_fsi_min = sum(r["metric_value"] for r in results) / len(results)
    std_fsi_min = math.sqrt(sum((r["metric_value"] - mean_fsi_min)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_fsi_min} std={std_fsi_min} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"FSI_min > 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")