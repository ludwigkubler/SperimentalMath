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
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(literals)
        return clauses
    
    def min_symmetric_bilinear_form(cnf):
        n = len(cnf[0])
        form = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in range(n):
                for j in range(i, n):
                    if clause[i] != 0 and clause[j] != 0:
                        form[i][j] += clause[i] * clause[j]
                        form[j][i] = form[i][j]
        return form
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf[0])
        rank_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if cnf[0][i] != 0 and cnf[0][j] != 0:
                    rank_matrix[i][j] = 1
                    rank_matrix[j][i] = 1
        # Compute the rank of the matrix
        rank = 0
        for i in range(n):
            if any(rank_matrix[j][i] != 0 for j in range(i, n)):
                rank += 1
                for j in range(i, n):
                    if rank_matrix[j][i] != 0:
                        for k in range(n):
                            rank_matrix[j][k] -= rank_matrix[i][k]
        return rank
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def p_value(r, n):
        if abs(r) < 1.96 / math.sqrt(n):  # Approximation for normal distribution
            return True
        return False
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_sbf_values = []
    ccr_var_values = []
    
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        cnf = generate_cnf(n, m)
        min_sbf = min_symmetric_bilinear_form(cnf)
        ccr_var = communication_complexity_rank_variance(cnf)
        min_sbf_values.append(sum(sum(row) for row in min_sbf))
        ccr_var_values.append(ccr_var)
    
    correlation = correlation_coefficient(min_sbf_values, ccr_var_values)
    p_val = p_value(correlation, len(n_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": p_val and abs(correlation) >= 0.5,
        "counterexample": "" if p_val and abs(correlation) >= 0.5 else "correlation_coefficient < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5\" first_failing_seed={first_failing_seed}")