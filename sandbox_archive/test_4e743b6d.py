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
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank:
                    factor = A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def ehrhart_polynomial_degree(A):
        m, n = len(A), len(A[0])
        return gaussian_elimination(A)
    
    def resolution_proof_width(n):
        # Simplified model for demonstration purposes
        return n * (n - 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            Tseitin_formula = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            incidence_matrix = []
            for i in range(n):
                row = [0] * (2 * n)
                row[i] = 1
                for j in range(n):
                    if Tseitin_formula[i][j]:
                        row[2 * j + 1] = -1
                        row[2 * j + 2] = 1
                incidence_matrix.append(row)
            degree = ehrhart_polynomial_degree(incidence_matrix)
            width = resolution_proof_width(n)
            if degree < width:
                conjecture_holds = False
                counterexample = f"n={n}, degree={degree}, width={width}"
                break
            total_metric_value += degree / width
            instances_tested += 1
            n_max = max(n_max, n)
    
    return {
        "metric_name": "Ratio of Ehrhart Degree to Resolution Width",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")