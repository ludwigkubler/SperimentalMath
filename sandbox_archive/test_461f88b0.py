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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                    i_max = i
            if matrix[i_max][j] == 0:
                continue
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for i in range(m):
                if i != rank:
                    factor = -matrix[i][j] / matrix[rank][j]
                    for k in range(n):
                        matrix[i][k] += factor * matrix[rank][k]
            rank += 1
        return rank
    
    def resolution_width(cnf):
        stack = []
        visited = set()
        for clause in cnf:
            if any(abs(lit) not in visited for lit in clause):
                stack.append(clause)
                visited.update(abs(lit) for lit in clause)
        while stack:
            clause1 = stack.pop()
            clause2 = next((c for c in cnf if any(-lit in c for lit in clause1)), None)
            if not clause2:
                return len(stack) + 1
            new_clause = [lit for lit in clause1 if lit not in clause2] + [lit for lit in clause2 if -lit not in clause1]
            stack.append(new_clause)
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        dim_K = gaussian_elimination([[int(lit != 0) for lit in clause] for clause in cnf])
        w_phi = resolution_width(cnf)
        results.append((dim_K, w_phi))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    dim_Ks, w_phis = zip(*results)
    mean_dim_K = sum(dim_Ks) / len(dim_Ks)
    mean_w_phi = sum(w_phis) / len(w_phis)
    correlation_coefficient = sum((dim_K - mean_dim_K) * (w_phi - mean_w_phi) for dim_K, w_phi in results) / (len(results) * math.sqrt(sum((dim_K - mean_dim_K)**2 for dim_K in dim_Ks)) * math.sqrt(sum((w_phi - mean_w_phi)**2 for w_phi in w_phis)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")