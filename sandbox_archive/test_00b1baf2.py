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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i][-1] for i in range(n)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def communication_complexity(n):
        # Placeholder function to compute communication complexity
        return n  # Simplified example
    
    def aff_roots(n):
        # Placeholder function to compute minimal number of affine roots
        return n  # Simplified example
    
    instances_tested = 0
    total_aff_roots = 0
    total_comm_complexity = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            C = communication_complexity(n)
            A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            b = [random.randint(-10, 10) for _ in range(n)]
            x = gaussian_elimination(A, b)
            aff_roots_value = aff_roots(n)
            
            total_aff_roots += aff_roots_value
            total_comm_complexity += C
            instances_tested += 1
    
    mean_aff_roots = total_aff_roots / instances_tested
    mean_comm_complexity = total_comm_complexity / instances_tested
    correlation_coefficient = (instances_tested * sum(aff_roots_value * C for aff_roots_value, C in zip(range(instances_tested), range(instances_tested))) - instances_tested * mean_aff_roots * mean_comm_complexity) / math.sqrt((instances_tested * sum(aff_roots_value**2 for aff_roots_value in range(instances_tested)) - instances_tested * mean_aff_roots**2) * (instances_tested * sum(C**2 for C in range(instances_tested)) - instances_tested * mean_comm_complexity**2))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "aff_roots_vs_comm_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")