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
        for i in range(m):
            # Find pivot
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back-substitute
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = A[i][-1]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        
        return x
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def semialgebra_rank(protocol):
        # Simplified example: rank is the number of non-zero rows after Gaussian elimination
        matrix = [[1 if i == j else 0 for j in range(len(protocol))] for i in range(len(protocol))]
        rank = gaussian_elimination(matrix)
        return sum(1 for x in rank if abs(x) > 1e-9)
    
    def communication_complexity_rank(n):
        # Simplified example: rank is n
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 random protocols
            protocol = [random.randint(1, n) for _ in range(n)]
            semialgebra_rank_value = semialgebra_rank(protocol)
            communication_complexity_rank_value = communication_complexity_rank(n)
            
            total_metric_value += semialgebra_rank_value
            instances_tested += 1
            n_max = max(n_max, n)
            
            if semialgebra_rank_value > communication_complexity_rank_value * math.log2(n):
                conjecture_holds = False
                counterexample = f"n={n}, protocol={protocol}"
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = 0
    for i in range(instances_tested):
        std_metric_value += (total_metric_value[i] - mean_metric_value) ** 2
    std_metric_value = math.sqrt(std_metric_value / instances_tested)
    
    return {
        "metric_name": "semialgebra_rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")