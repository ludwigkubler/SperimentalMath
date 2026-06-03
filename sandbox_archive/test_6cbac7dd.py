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
    
    def communication_matrix(f):
        n = int(math.log2(len(f)))
        C = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j] == 1:
                    C[i][j] = 1
        return C
    
    def matrix_rank(C):
        m, n = len(C), len(C[0])
        rank = 0
        for i in range(m):
            if any(C[j][i] != 0 for j in range(rank)):
                rank += 1
                for j in range(n):
                    C[i][j], C[rank-1][j] = C[rank-1][j], C[i][j]
        return rank
    
    def coxeter_group_action_complexity(f):
        n = int(math.log2(len(f)))
        complexity = 0
        for i in range(n):
            if any(f[j ^ (1 << i)] != f[j] for j in range(2**n)):
                complexity += 1
        return complexity
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    c_f_list = []
    r_C_f_list = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        C_f = communication_matrix(f)
        c_f = coxeter_group_action_complexity(f)
        r_C_f = matrix_rank(C_f)
        
        if len(c_f_list) >= 30:
            break
        
        c_f_list.append(c_f)
        r_C_f_list.append(r_C_f)
    
    if len(c_f_list) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(c_f_list),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation = pearson_correlation(c_f_list, r_C_f_list)
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(c_f_list),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_data")