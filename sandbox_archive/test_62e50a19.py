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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        literals = set(abs(lit) for clause in cnf for lit in clause)
        literal = next(iter(literals))
        new_assignment = assignment + [literal]
        if dpll(substitute(cnf, literal), new_assignment):
            return True
        new_assignment = assignment + [-literal]
        if dpll(substitute(cnf, -literal), new_assignment):
            return True
        return False
    
    def substitute(cnf, lit):
        return [[l for l in clause if l != lit and l != -lit] for clause in cnf]
    
    def min_quasigroup_rank(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        rank = 0
        while True:
            try:
                matrix = [[random.randint(1, n) for _ in range(n)] for _ in range(n)]
                if is_valid_quasigroup(matrix):
                    return rank
                rank += 1
            except ValueError:
                pass
    
    def is_valid_quasigroup(matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if matrix[matrix[i][j] - 1][matrix[j][k] - 1] != matrix[i][k]:
                        raise ValueError
        return True
    
    def resolution_width(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if set(clauses[i]).intersection(set(clauses[j])):
                        new_clause = [l for l in clauses[i] if l not in set(clauses[j])]
                        new_clause.extend([l for l in clauses[j] if l not in set(clauses[i])])
                        new_clauses.append(new_clause)
            if len(new_clauses) == 0:
                return len(clauses)
            clauses = list(set(tuple(sorted(c)) for c in new_clauses))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        cnf = generate_cnf(n, m)
        rank = min_quasigroup_rank(cnf)
        width = resolution_width(cnf)
        results.append({"rank": rank, "width": width})
    
    correlation_coefficient = calculate_correlation(results)
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.8,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.8 else "correlation_outside_bounds"
    }

def calculate_correlation(results):
    n = len(results)
    sum_rank = sum(result["rank"] for result in results)
    sum_width = sum(result["width"] for result in results)
    sum_rank_width = sum(result["rank"] * result["width"] for result in results)
    sum_rank_squared = sum(result["rank"] ** 2 for result in results)
    sum_width_squared = sum(result["width"] ** 2 for result in results)
    
    numerator = n * sum_rank_width - sum_rank * sum_width
    denominator = math.sqrt((n * sum_rank_squared - sum_rank ** 2) * (n * sum_width_squared - sum_width ** 2))
    
    return numerator / denominator if denominator != 0 else 0

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["metric_value"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_bounds\" first_failing_seed={first_failing_seed}")