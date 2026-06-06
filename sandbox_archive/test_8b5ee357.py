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
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def frobenius_index(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        V = []
        for c in clauses:
            v = [0] * (2 * len(cnf))
            for i, lit in enumerate(c):
                if lit > 0:
                    v[2 * i] = 1
                else:
                    v[2 * i + 1] = 1
            V.append(v)
        return min([sum(v) for v in V])
    
    def sat_clause_subset_complexity(cnf):
        return sum(len(c) for c in cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            cnf = generate_cnf(n, random.randint(1, 10 * n))
            min_index = frobenius_index(cnf)
            sat_complexity = sat_clause_subset_complexity(cnf)
            results.append((min_index, sat_complexity))
    
    if not results:
        return {
            "metric_name": "Spearman's Rank Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n_max = max(n_values)
    instances_tested = len(results)
    min_indices, sat_complexities = zip(*results)
    rho = calculate_spearman_rank_correlation(min_indices, sat_complexities)
    
    return {
        "metric_name": "Spearman's Rank Correlation Coefficient",
        "metric_value": rho,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": rho >= 0.8 and all(rho >= -0.5 for _ in range(instances_tested)),
        "counterexample": ""
    }

def calculate_spearman_rank_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    ranks_x = {val: rank for rank, val in enumerate(sorted(set(x)), start=1)}
    ranks_y = {val: rank for rank, val in enumerate(sorted(set(y)), start=1)}
    
    sum_differences_squared = sum((ranks_x[x[i]] - ranks_y[y[i]]) ** 2 for i in range(n))
    rho_numerator = n * (n**2 - 1) - 6 * sum_differences_squared
    rho_denominator = (n * (n**2 - 1)) ** 0.5
    
    if rho_denominator == 0:
        return None
    
    return rho_numerator / rho_denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["instances_tested"] > 0 for r in results):
        print("RESULT: INCONCLUSIVE reason=not_enough_instances")
    else:
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        std_rho = (sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
        elif any(r["metric_value"] < -0.5 for r in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='rho < -0.5' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=not_enough_support")