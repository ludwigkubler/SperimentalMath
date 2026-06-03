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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix(f):
        n = int(math.log2(len(f)))
        C_f = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j] == f[i]:
                    C_f[i][j] = 1
        return C_f
    
    def matrix_rank(C_f):
        n = len(C_f)
        rank = 0
        for i in range(n):
            pivot_row = -1
            for r in range(i, n):
                if C_f[r][i] != 0:
                    pivot_row = r
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for j in range(n):
                C_f[i][j], C_f[pivot_row][j] = C_f[pivot_row][j], C_f[i][j]
            for r in range(n):
                if r != i and C_f[r][i] != 0:
                    factor = Fraction(C_f[r][i], C_f[i][i])
                    for j in range(n):
                        C_f[r][j] -= factor * C_f[i][j]
        return rank
    
    def coxeter_group_action_complexity(f):
        n = int(math.log2(len(f)))
        complexity = 0
        for i in range(1, n + 1):
            if all(f[j ^ k] == f[j] for j in range(2**n) for k in range(1 << i)):
                complexity += 1
        return complexity
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        var_x = sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x)
        var_y = sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y)
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    c_f_values = []
    r_C_f_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        C_f = communication_matrix(f)
        c_f = coxeter_group_action_complexity(f)
        r_C_f = matrix_rank(C_f)
        
        c_f_values.append(c_f)
        r_C_f_values.append(r_C_f)
    
    correlation_coefficient = pearson_correlation(c_f_values, r_C_f_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": "" if correlation_coefficient >= 0.9 else f"Correlation coefficient: {correlation_coefficient}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_correlation_coefficient = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation_coefficient} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")