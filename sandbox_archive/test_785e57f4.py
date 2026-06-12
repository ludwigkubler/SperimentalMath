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

def p_adic_dilogarithm(x, p):
    if x <= 0:
        return 0
    result = 0
    power = 1
    while True:
        term = power / (p ** power)
        if abs(term) < 1e-10:
            break
        result += term * math.log(x + p ** (-power))
        power += 1
    return result

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row[:] + [0] for row in matrix]
    for i in range(m):
        augmented_matrix[i][n] = 1 if i == 0 else 0
    for j in range(n):
        pivot_row = -1
        for i in range(j, m):
            if abs(augmented_matrix[i][j]) > 1e-10:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        augmented_matrix[pivot_row], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[pivot_row]
        for i in range(m):
            if i != j:
                factor = augmented_matrix[i][j] / augmented_matrix[j][j]
                for k in range(n + 1):
                    augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
    rank = sum(1 for row in augmented_matrix if any(abs(x) > 1e-10 for x in row[:n]))
    return rank

def generate_formula(n):
    literals = [f'x{i}' for i in range(n)]
    formula = ' or '.join(random.sample(literals, random.randint(1, n)))
    return formula

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "MinRank_p vs Resolution Proof Width"
    instances_tested = 0
    n_max = 0
    MinRank_p_values = []
    w_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_formula(n)
            MinRank_p = rank([[p_adic_dilogarithm(eval(lit), 2) for lit in formula.split(' or ')]])
            w = len(formula.split(' or '))
            
            MinRank_p_values.append(MinRank_p)
            w_values.append(w)
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not MinRank_p_values:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_M = sum(MinRank_p_values) / len(MinRank_p_values)
    mean_w = sum(w_values) / len(w_values)
    covariance = sum((MinRank_p_values[i] - mean_M) * (w_values[i] - mean_w) for i in range(len(MinRank_p_values))) / len(MinRank_p_values)
    variance_M = sum((MinRank_p_values[i] - mean_M) ** 2 for i in range(len(MinRank_p_values))) / len(MinRank_p_values)
    variance_w = sum((w_values[i] - mean_w) ** 2 for i in range(len(w_values))) / len(w_values)
    
    correlation_coefficient = covariance / math.sqrt(variance_M * variance_w)
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.9 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")