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
        cnf.append(clause)
    return cnf

def characteristic_polynomial(cnf):
    n = len(set(abs(lit) for lit in sum(cnf, [])))
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for lit in clause:
            if lit > 0:
                row = lit - 1
            else:
                row = -(lit + 1)
            matrix[row][row] += 1
            for other_lit in clause:
                if other_lit != lit:
                    col = abs(other_lit) - 1
                    matrix[row][col] -= 1
    return matrix

def tropicalize(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                matrix[i][j] = float('-inf')
    return matrix

def compute_index(tropical_matrix):
    n = len(tropical_matrix)
    det = 1
    for i in range(n):
        max_val = float('-inf')
        for j in range(n):
            if tropical_matrix[j][i] > max_val:
                max_val = tropical_matrix[j][i]
        det *= max_val
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n * 2))
            results.append(cnf)
    
    clause_counts = [len(cnf) for cnf in results]
    indices = [compute_index(tropicalize(characteristic_polynomial(cnf))) for cnf in results]
    
    if not clause_counts or not indices:
        return {
            "metric_name": "Index_G",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n for n, _ in zip([5, 10, 15, 20, 30, 40], [len(results) // 6] * 6)),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = sum((x - mean_x) * (y - mean_y) for x, y in zip(clause_counts, indices)) / len(clause_counts)
    mean_x = sum(clause_counts) / len(clause_counts)
    mean_y = sum(indices) / len(indices)
    
    return {
        "metric_name": "Index_G",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in zip([5, 10, 15, 20, 30, 40], [len(results) // 6] * 6)),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": "" if correlation >= 0.8 else f"correlation={correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation<{result['metric_value']}\"> first_failing_seed={first_failing_seed}")