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
    
    def matrix_representation(f, n):
        M = [[f[i ^ j] for j in range(2**n)] for i in range(2**n)]
        return M
    
    def rank_variance(M):
        n = len(M)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [M[i] + I[i] for i in range(n)]
        det_A = determinant(A, n)
        return abs(det_A) / n
    
    def determinant(matrix, n):
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1)**j * matrix[0][j] * determinant(submatrix, n-1)
        return det
    
    def is_automorphic_form(f, M):
        n = len(M)
        for i in range(n):
            if f[i] != M[i][i]:
                return False
        return True
    
    def count_automorphic_forms(M):
        n = len(M)
        count = 0
        for i in range(n):
            if is_automorphic_form(i, M):
                count += 1
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        M = matrix_representation(f, n)
        rho_f = rank_variance(M)
        aut_f = count_automorphic_forms(M)
        results.append({"n": n, "rho_f": rho_f, "aut_f": aut_f})
    
    if len(results) < 30:
        return {
            "metric_name": "rank_variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    rho_f_values = [r["rho_f"] for r in results]
    aut_f_values = [r["aut_f"] for r in results]
    
    mean_rho_f = sum(rho_f_values) / len(rho_f_values)
    std_rho_f = math.sqrt(sum((x - mean_rho_f)**2 for x in rho_f_values) / len(rho_f_values))
    mean_aut_f = sum(aut_f_values) / len(aut_f_values)
    std_aut_f = math.sqrt(sum((x - mean_aut_f)**2 for x in aut_f_values) / len(aut_f_values))
    
    correlation_coefficient = (sum((rho_f_values[i] - mean_rho_f) * (aut_f_values[i] - mean_aut_f) for i in range(len(rho_f_values))) /
                               (len(rho_f_values) * std_rho_f * std_aut_f))
    
    return {
        "metric_name": "rank_variance",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print("RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")