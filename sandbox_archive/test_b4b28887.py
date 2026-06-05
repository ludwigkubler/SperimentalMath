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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def tropical_polynomial(clauses):
        phi_n = {}
        for clause in clauses:
            degree = sum(abs(coeff) for coeff in clause)
            if degree not in phi_n:
                phi_n[degree] = 0
            phi_n[degree] += 1
        return phi_n
    
    def minimal_monomial_degree(phi_n):
        return min(phi_n.keys()) if phi_n else None
    
    def clause_entropy(clauses):
        counts = [0] * (len(max(clauses, key=len)) + 1)
        for clause in clauses:
            counts[len(clause)] += 1
        total_clauses = len(clauses)
        entropy = 0.0
        for count in counts:
            if count > 0:
                p = Fraction(count, total_clauses)
                entropy -= p * math.log2(p)
        return entropy
    
    def spearman_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i + 1 for i in range(n)}
        rank_y = {y[i]: i + 1 for i in range(n)}
        d_squared_sum = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_sat_instance(n)
        phi_n = tropical_polynomial(clauses)
        d_n = minimal_monomial_degree(phi_n)
        H_phi_n = clause_entropy(clauses)
        
        if d_n is not None and H_phi_n > 0:
            results.append((d_n, H_phi_n))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    d_values, H_values = zip(*results)
    rho = spearman_correlation(d_values, H_values)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": rho >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.8 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < 0.8))]
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")