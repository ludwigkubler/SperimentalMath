# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def communication_matrix(f):
        n = int(math.log2(len(f)))
        C = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i ^ j] == 1:
                    C[i][j] = 1
        return C
    
    def matrix_rank(C):
        n = len(C)
        rank = 0
        for i in range(n):
            pivot = next((j for j in range(i, n) if C[j][i] != 0), None)
            if pivot is None:
                continue
            rank += 1
            for j in range(n):
                if j == pivot:
                    continue
                factor = C[j][i] / C[pivot][i]
                for k in range(n):
                    C[j][k] -= factor * C[pivot][k]
        return rank
    
    def action_complexity(C):
        n = len(C)
        generators = []
        for i in range(n):
            if any(C[i][j] != 0 for j in range(i+1, n)):
                generators.append(i)
        return len(generators)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_c_f = 0
    total_r_C_f = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        C_f = communication_matrix(f)
        c_f = action_complexity(C_f)
        r_C_f = matrix_rank(C_f)
        
        instances_tested += len(f)
        total_c_f += c_f
        total_r_C_f += r_C_f
    
    mean_c_f = total_c_f / instances_tested
    mean_r_C_f = total_r_C_f / instances_tested
    
    correlation_coefficient = (instances_tested * sum(c_f * r_C_f for c_f, r_C_f in zip(range(1, n_values[-1]+1), range(1, n_values[-1]+1))) -
                               mean_c_f * instances_tested - mean_r_C_f * instances_tested) / \
                              math.sqrt((instances_tested * sum(c_f**2 for c_f in range(1, n_values[-1]+1)) - mean_c_f**2) *
                                        (instances_tested * sum(r_C_f**2 for r_C_f in range(1, n_values[-1]+1)) - mean_r_C_f**2))
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")