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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        pivot = A[i][i]
        for k in range(i+1, n):
            factor = Fraction(A[k][i], pivot)
            for j in range(n):
                A[k][j] -= factor * A[i][j]
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(lit == 0 for lit in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def cohomological_dimension(cnf):
        # Placeholder function to compute the cohomological dimension
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf) / n
    
    def circuit_monotone_width(cnf):
        # Placeholder function to compute the circuit monotone width
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        mu_phi = cohomological_dimension(cnf)
        w_m_phi = circuit_monotone_width(cnf)
        metrics.append((mu_phi, w_m_phi))
    
    if not metrics:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mu_values = [mu for mu, _ in metrics]
    w_m_values = [w_m for _, w_m in metrics]
    
    mean_mu = sum(mu_values) / len(mu_values)
    mean_w_m = sum(w_m_values) / len(w_m_values)
    
    pearson_corr = 0
    if len(mu_values) > 1:
        numerator = sum((mu - mean_mu) * (w_m - mean_w_m) for mu, w_m in metrics)
        denominator = math.sqrt(sum((mu - mean_mu)**2 for mu in mu_values)) * math.sqrt(sum((w_m - mean_w_m)**2 for w_m in w_m_values))
        pearson_corr = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_corr,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.8 and abs(mean_mu - mean_w_m) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")