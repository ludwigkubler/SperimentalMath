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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] * clause[j] < 0 for i in range(n) for j in range(i + 1, n)):
                cnf.append(clause)
        return cnf
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf[0])
        rank_matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in range(n):
                for j in range(i + 1, n):
                    if clause[i] * clause[j] < 0:
                        rank_matrix[i][j] += 1
                        rank_matrix[j][i] += 1
        return sum(sum(row) for row in rank_matrix) / (n * (n - 1))
    
    def min_symmetric_bilinear_form(cnf):
        n = len(cnf[0])
        bilinear_form = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in range(n):
                for j in range(i + 1, n):
                    if clause[i] * clause[j] < 0:
                        bilinear_form[i][j] += 1
                        bilinear_form[j][i] += 1
        return sum(sum(row) for row in bilinear_form) / (n * (n - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_sbf_values = []
    ccr_var_values = []
    
    for n in n_values:
        cnf = generate_cnf(n, int(1.5 * n))
        min_sbf_values.append(min_symmetric_bilinear_form(cnf))
        ccr_var_values.append(communication_complexity_rank_variance(cnf))
    
    if not min_sbf_values or not ccr_var_values:
        return {
            "metric_name": "min_SBF vs CCR_var",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_cnf"
        }
    
    correlation_coefficient = sum((min_sbf_values[i] - sum(min_sbf_values) / len(min_sbf_values)) * 
                                  (ccr_var_values[i] - sum(ccr_var_values) / len(ccr_var_values))
                                 for i in range(len(min_sbf_values))) / \
                               (len(min_sbf_values) * math.sqrt(sum((x - sum(min_sbf_values) / len(min_sbf_values)) ** 2 
                                                                    for x in min_sbf_values)) *
                                math.sqrt(sum((y - sum(ccr_var_values) / len(ccr_var_values)) ** 2 
                                             for y in ccr_var_values)))
    
    return {
        "metric_name": "min_SBF vs CCR_var",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_sbf_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                                            31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
                                            73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 
                                     for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.5) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"]) < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_corr_coeff' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")