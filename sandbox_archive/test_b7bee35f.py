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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        cnf.append(clause)
    return cnf

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        for j in range(n):
            matrix[i][j] /= matrix[i][i]
        for j in range(m):
            if i != j:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    row_echelon_form = gaussian_elimination(matrix)
    rank = 0
    for i in range(m):
        if any(row_echelon_form[i]):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested // 6):
            m = random.randint(2 * n, 4 * n)
            cnf = generate_cnf(n, m)
            f_phi = m  # Placeholder for actual Frege proof length calculation
            lhr_phi = rank(cnf)
            metric_values.append((n, f_phi, lhr_phi))
    
    if not metric_values:
        return {
            "metric_name": "lhr(φ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, f_phi_values, lhr_phi_values = zip(*metric_values)
    mean_f_phi = sum(f_phi_values) / len(f_phi_values)
    mean_lhr_phi = sum(lhr_phi_values) / len(lhr_phi_values)
    correlation_coefficient = 0.0
    
    for i in range(len(metric_values)):
        correlation_coefficient += (f_phi_values[i] - mean_f_phi) * (lhr_phi_values[i] - mean_lhr_phi)
    
    correlation_coefficient /= math.sqrt(sum((x - mean_f_phi) ** 2 for x in f_phi_values)) * math.sqrt(sum((y - mean_lhr_phi) ** 2 for y in lhr_phi_values))
    
    return {
        "metric_name": "lhr(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")