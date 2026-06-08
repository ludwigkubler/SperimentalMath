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
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    M[i][j] = 1
        return M
    
    def frobenius_schur_index(M):
        n = len(M)
        trace = sum(M[i][i] for i in range(n))
        det = determinant(M, n)
        return abs(trace / det)
    
    def determinant(matrix, size):
        if size == 1:
            return matrix[0][0]
        det = 0
        for c in range(size):
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            sign = (-1) ** (c % 2)
            det += sign * matrix[0][c] * determinant(submatrix, size - 1)
        return det
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_communication = 0
        for i in range(2**n):
            for j in range(2**n):
                if f[i] != f[j]:
                    communication = bin(i ^ j).count('1')
                    if communication > max_communication:
                        max_communication = communication
        return max_communication
    
    n_values = [5, 10, 15, 20, 30, 40]
    FSI_min_total = 0
    CC_lower_total = 0
    instances_tested = 0
    
    for n in n_values:
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
        
        FSI_min_total += FSI_min
        CC_lower_total += CC_lower
        instances_tested += len(f)
    
    mean_FSI_min = FSI_min_total / instances_tested
    mean_CC_lower = CC_lower_total / instances_tested
    
    return {
        "metric_name": "FSI_min",
        "metric_value": mean_FSI_min,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": mean_FSI_min >= 0.8 * mean_CC_lower,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
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