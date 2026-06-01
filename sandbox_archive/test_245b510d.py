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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_sat_instance(k, m):
        variables = set()
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(k), k)]
            clauses.append(clause)
            for var in clause:
                variables.add(abs(var))
        return len(variables), clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for j in range(cols):
            i_max = rank
            for i in range(rank + 1, rows):
                if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                    i_max = i
            if matrix[i_max][j] != 0:
                matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
                for i in range(rank + 1, rows):
                    factor = -matrix[i][j] / matrix[rank][j]
                    for k in range(j, cols):
                        if rank == i and matrix[i][k]:
                            return None
                        matrix[i][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    def clause_set_complexity(clauses):
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        return len(literals)
    
    n_min, n_max = 5, 40
    instances_tested = 0
    R_local_values = []
    S_clauses_values = []
    
    for n in range(n_min, n_max + 1):
        for _ in range(30 // (n - n_min + 1)):
            k = random.randint(2, min(n, 5))
            m = random.randint(k * 2, n)
            num_vars, clauses = generate_k_sat_instance(k, m)
            matrix = [[int(lit == j) for j in range(num_vars)] for clause in clauses for lit in clause]
            rank = gaussian_elimination(matrix)
            if rank is not None:
                R_local_values.append(rank)
                S_clauses_values.append(clause_set_complexity(clauses))
                instances_tested += 1
    
    if not R_local_values or not S_clauses_values:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Empty matrix or clauses"
        }
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = (sum((xi - mean_x) ** 2 for xi in x) / len(x)) ** 0.5
        std_y = (sum((yi - mean_y) ** 2 for yi in y) / len(y)) ** 0.5
        return cov_xy / (std_x * std_y)
    
    correlation_coefficient = pearson_correlation(R_local_values, S_clauses_values)
    conjecture_holds = correlation_coefficient >= 0.8
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Correlation < 0.8: {correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")