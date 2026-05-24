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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_xor_tautology(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropical_derivative(tau):
        n = len(tau)
        D = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n + 1):
                if tau[i] == tau[j]:
                    D[i][j] = max(D[i-1][j], D[i][j-1]) + 1
                else:
                    D[i][j] = max(D[i-1][j], D[i][j-1])
        return D[n][n]
    
    def resolution_length(tau):
        n = len(tau)
        clauses = [tau[i:i+2] for i in range(0, n, 2)]
        proof = []
        while True:
            new_clauses = []
            for clause in clauses:
                if len(clause) == 1:
                    return len(proof)
                for other_clause in clauses:
                    if set(clause).isdisjoint(set(other_clause)):
                        continue
                    new_clause = list(set(clause) ^ set(other_clause))
                    if new_clause not in proof and new_clause not in new_clauses:
                        new_clauses.append(new_clause)
            if not new_clauses:
                return len(proof)
            clauses.extend(new_clauses)
            proof.extend(new_clauses)
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        x_sorted = sorted(range(n), key=lambda i: x[i])
        y_sorted = sorted(range(n), key=lambda i: y[i])
        rank_x = [x_sorted.index(i) for i in range(n)]
        rank_y = [y_sorted.index(i) for i in range(n)]
        n = len(x)
        sum_diff_squared = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        rho = 1 - (6 * sum_diff_squared) / (n * (n**2 - 1))
        return rho
    
    def polynomial_regression(x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        xx_sum = sum((x[i] - x_mean) ** 2 for i in range(n))
        xy_sum = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        slope = xy_sum / xx_sum
        intercept = y_mean - slope * x_mean
        return slope, intercept
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        tau = generate_xor_tautology(n)
        D = tropical_derivative(tau)
        r = resolution_length(tau)
        results.append((n, D, r))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    D_values = [result[1] for result in results]
    r_values = [result[2] for result in results]
    rho = spearman_rank_correlation(D_values, r_values)
    
    if rho < 0.7:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": rho,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Spearman rank correlation {rho} is less than 0.7"
        }
    
    slope, intercept = polynomial_regression(D_values, r_values)
    if not (slope > 0 and intercept == 0):
        return {
            "metric_name": "Polynomial Regression",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "polynomial_regression_not_of_form_Theta(log_n)"
        }
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation less than 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")