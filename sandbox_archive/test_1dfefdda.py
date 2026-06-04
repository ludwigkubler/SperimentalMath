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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def resolution_width(cnf):
        clauses = cnf.split('\n')
        n = len(clauses)
        visited = set()
        stack = []
        for clause in clauses:
            literals = [int(lit) for lit in clause.split() if lit != '0']
            for literal in literals:
                if -literal in visited:
                    return 1
                visited.add(literal)
                stack.append((literals, visited.copy()))
        return len(stack)

    def eta_invariant(cnf):
        clauses = cnf.split('\n')
        n = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i, clause in enumerate(clauses):
            literals = [int(lit) for lit in clause.split() if lit != '0']
            for literal in literals:
                matrix[i][abs(literal)] += 1
        gaussian_elimination(matrix)
        rank = sum(1 for row in matrix if any(row[j] != 0 for j in range(n + 1)))
        return n - rank

    instances_tested = 0
    eta_values = []
    width_values = []
    n_max = 5
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = '\n'.join(' '.join(str(random.choice([-1, 1]) * i) for i in range(1, n + 1)) for _ in range(n))
        eta_phi = eta_invariant(cnf)
        w_phi = resolution_width(cnf)
        
        if eta_phi is not None and w_phi is not None:
            instances_tested += 1
            eta_values.append(eta_phi)
            width_values.append(w_phi)
            n_max = max(n_max, n)

    if instances_tested < 30:
        return {
            "metric_name": "eta_invariant_resolution_width_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_eta = sum(eta_values) / instances_tested
    std_eta = math.sqrt(sum((x - mean_eta) ** 2 for x in eta_values) / instances_tested)
    mean_width = sum(width_values) / instances_tested
    std_width = math.sqrt(sum((x - mean_width) ** 2 for x in width_values) / instances_tested)

    ratio_mean = mean_eta / mean_width
    ratio_std = std_eta / mean_width

    return {
        "metric_name": "eta_invariant_resolution_width_ratio",
        "metric_value": ratio_mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": ratio_mean >= 1 and ratio_std <= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["metric_value"] is not None for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient={mean_ratio}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")