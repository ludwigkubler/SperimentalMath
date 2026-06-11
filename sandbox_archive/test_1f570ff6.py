# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = Fraction(A[i][i])
        for j in range(i, n):
            A[i][j] /= factor
        
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def local_induction_dimension(C):
    n = len(C)
    A = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if C[i][j]:
                A[i][j] = Fraction(1, C[i][j])
    return determinant(gaussian_elimination(A))

def communication_complexity_rank_variance(C):
    n = len(C)
    rank = sum(sum(row) > 0 for row in C)
    variance = (rank - n / 2) ** 2
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        C = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        lid = local_induction_dimension(C)
        variance = communication_complexity_rank_variance(C)
        results.append((lid, variance))
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    mean_lid = sum(l for l, v in results) / len(results)
    median_lid = sorted([l for l, v in results])[len(results) // 2]
    correlation = sum((l - mean_lid) * (v - variance) for l, v in results) / len(results)
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation) >= 0.8 and abs(mean_lid - median_lid) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")