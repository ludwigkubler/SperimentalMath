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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
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

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll_search_tree_height(phi, variables):
    if not phi:
        return 0
    if len(phi) == 1:
        return 1
    variable = random.choice(variables)
    true_branch = [x for x in phi if variable in x]
    false_branch = [x for x in phi if variable not in x]
    return 1 + max(dpll_search_tree_height(true_branch, variables), dpll_search_tree_height(false_branch, variables))

def kahler_class_rank(phi):
    n = len(phi)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j:
                A[i][j] = random.choice([-1, 1])
                b[j] += A[i][j]
    gaussian_elimination(A, b)
    rank = sum(1 for row in A if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        kr_sum = 0
        h_sum = 0
        
        while instances_tested < 30:
            phi = [[random.choice([-i, i]) for _ in range(random.randint(1, n))] for _ in range(n)]
            variables = list(range(1, n + 1))
            kr = kahler_class_rank(phi)
            h = dpll_search_tree_height(phi, variables)
            
            if kr == 0 or h == 0:
                continue
            
            kr_sum += kr
            h_sum += h
            instances_tested += 1
        
        mean_kr = Fraction(kr_sum, instances_tested)
        mean_h = Fraction(h_sum, instances_tested)
        
        correlation_coefficient = (instances_tested * sum(mean_kr * mean_h for _ in range(instances_tested)) - instances_tested * mean_kr * mean_h) / \
                                  ((instances_tested - 1) * (mean_kr ** 2 + mean_h ** 2 - 2 * mean_kr * mean_h))
        
        results.append({
            "n": n,
            "kr_sum": kr_sum,
            "h_sum": h_sum,
            "correlation_coefficient": correlation_coefficient
        })
    
    total_instances_tested = sum(result["instances_tested"] for result in results)
    mean_correlation_coefficient = sum(result["correlation_coefficient"] * result["instances_tested"] for result in results) / total_instances_tested
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(mean_correlation_coefficient),
        "instances_tested": total_instances_tested,
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(mean_correlation_coefficient - 1.0) <= 0.05,
        "counterexample": "" if mean_correlation_coefficient >= 0.95 else f"Correlation coefficient {mean_correlation_coefficient} is not close to 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{results[sum(1 for result in results if not result['conjecture_holds'])].get('counterexample', 'unknown')}\") first_failing_seed={seeds[sum(1 for result in results if not result['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")