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
    
    def log_det(matrix):
        n = len(matrix)
        if n == 1:
            return math.log(abs(matrix[0][0]))
        
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * log_det(submatrix)
        return det
    
    def tensor_product(matrices):
        if len(matrices) == 1:
            return matrices[0]
        result = matrices[0]
        for i in range(1, len(matrices)):
            new_result = []
            for r1 in result:
                for r2 in matrices[i]:
                    new_row = [sum(a * b for a, b in zip(r1[j], r2[k])) for j in range(len(r1)) for k in range(len(r2))]
                    new_result.append(new_row)
            result = new_result
        return result
    
    n = 16
    M_P = [[random.random() for _ in range(n)] for _ in range(n)]
    for row in M_P:
        total = sum(row)
        if total == 0:
            continue
        for i in range(n):
            row[i] /= total
    
    rho_values = []
    for i in range(1, n + 1):
        M_P_i = tensor_product([M_P] * i)
        det = log_det(M_P_i)
        if det <= 0:
            continue
        rho_values.append(-math.log(det) / n)
    
    if not rho_values:
        return {
            "metric_name": "rho",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No valid rho values found"
        }
    
    min_rho = min(rho_values)
    metric_value = min_rho
    conjecture_holds = min_rho >= 0.3 * math.log(n)
    counterexample = "" if conjecture_holds else f"Min rho {min_rho} < 0.3 log n = {0.3 * math.log(n)}"
    
    return {
        "metric_name": "rho",
        "metric_value": metric_value,
        "instances_tested": len(rho_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Min rho < 0.3 log n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=No valid rho values found")