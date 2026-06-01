# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_planar(graph):
        # Implement planarity test (e.g., Kuratowski's theorem check)
        return True  # Placeholder for actual implementation
    
    def lll_reduction(matrix):
        # Implement LLL reduction algorithm
        n = len(matrix)
        B = [list(row) for row in matrix]
        u = [1] * n
        d = [1] * n
        
        for k in range(1, n):
            b_k = B[k]
            for j in range(k - 1, -1, -1):
                alpha = Fraction(sum(b_k[i] * B[j][i] for i in range(len(b_k))), u[j])
                if abs(alpha) >= 3/4:
                    b_k = [b_k[i] - (alpha * B[j][i]) for i in range(len(b_k))]
                    d[k] -= alpha * d[j]
                    u[k] -= alpha * u[j]
            B[k] = b_k
            beta = Fraction(sum(B[k][i]**2 for i in range(k)), d[k])
            if k > 1 and beta >= (3/4)**2:
                B[k], B[k - 1] = B[k - 1], B[k]
                u[k], u[k - 1] = u[k - 1], u[k]
                d[k], d[k - 1] = d[k - 1], d[k]
        
        return [list(row) for row in B]
    
    def communication_complexity(graph):
        # Implement communication complexity calculation
        return len(graph)  # Placeholder for actual implementation
    
    def minimal_diophantine_degree(matrix):
        # Implement minimal diophantine degree calculation using LLL reduction
        reduced_matrix = lll_reduction(matrix)
        rank = sum(1 for row in reduced_matrix if any(x != 0 for x in row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    dd_values = []
    ccr_values = []
    
    for n in n_values:
        graph = [[random.randint(0, 1) if i != j else 0 for j in range(n)] for i in range(n)]
        if not is_planar(graph):
            continue
        
        dd_G = minimal_diophantine_degree(graph)
        ccr_G = communication_complexity(graph)
        
        dd_values.append(dd_G)
        ccr_values.append(ccr_G)
    
    if len(dd_values) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(dd_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    mean_dd = sum(dd_values) / len(dd_values)
    mean_ccr = sum(ccr_values) / len(ccr_values)
    correlation_coefficient = sum((dd - mean_dd) * (ccr - mean_ccr) for dd, ccr in zip(dd_values, ccr_values)) / (len(dd_values) * math.sqrt(sum((dd - mean_dd)**2 for dd in dd_values) * sum((ccr - mean_ccr)**2 for ccr in ccr_values)))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(dd_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and correlation_coefficient <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={result['seed']}")
                break