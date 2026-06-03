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

def gaussian_elimination(matrix):
    n = len(matrix)
    m = len(matrix[0])
    rank = 0
    
    for i in range(n):
        if rank >= m:
            break
        
        pivot_row = i
        while matrix[pivot_row][i] == 0:
            pivot_row += 1
            if pivot_row == n:
                pivot_row = i
                break
        
        if matrix[pivot_row][i] == 0:
            continue
        
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        for j in range(n):
            if j != i and matrix[j][i] != 0:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
        
        rank += 1
    
    return rank

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity(f):
    n = int(math.log2(len(f)))
    inputs = [(i >> j) & 1 for i in range(2**n) for j in range(n)]
    outputs = f[:]
    return max(sum(inputs[i] == outputs[i] for i in range(2**n)), sum(inputs[i] != outputs[i] for i in range(2**n)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    comm_complexities = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        S = construct_symplectic_matrix(f, n)
        rank = gaussian_elimination(S)
        C_f = communication_complexity(f)
        
        min_ranks.append(rank)
        comm_complexities.append(C_f)
    
    mean_rank = sum(min_ranks) / len(min_ranks)
    mean_C_f = sum(comm_complexities) / len(comm_complexities)
    abs_diffs = [abs(r - C_f) for r, C_f in zip(min_ranks, comm_complexities)]
    mean_abs_diff = sum(abs_diffs) / len(abs_diffs)
    
    correlation_coefficient = 0
    if len(min_ranks) > 1 and len(comm_complexities) > 1:
        numerator = sum((min_ranks[i] - mean_rank) * (comm_complexities[i] - mean_C_f) for i in range(len(min_ranks)))
        denominator = math.sqrt(sum((min_ranks[i] - mean_rank)**2 for i in range(len(min_ranks)))) * math.sqrt(sum((comm_complexities[i] - mean_C_f)**2 for i in range(len(comm_complexities))))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or mean_abs_diff > 3"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")