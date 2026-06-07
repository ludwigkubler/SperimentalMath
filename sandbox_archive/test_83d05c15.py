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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def polynomial_evaluation(poly, x):
        result = 0
        for coeff in poly:
            result = (result * 2 + coeff) % 2
        return result
    
    def characteristic_polynomial(f):
        n = len(f)
        phi_f = [1]
        for i in range(1, n+1):
            new_term = []
            for j in range(len(phi_f)):
                new_term.append((phi_f[j] * f[i-1]) % 2)
            phi_f.extend(new_term)
        return phi_f
    
    def adjoint_group_order(poly):
        n = len(poly)
        if poly[0] != 1:
            return None
        for i in range(1, n+1):
            if poly[i] == 1:
                return i
        return None
    
    def circuit_entanglement_complexity(f):
        n = len(f)
        # Simplified model: complexity is the number of non-zero terms in the polynomial
        return sum(1 for term in f if term != 0)
    
    def spearman_correlation(ranks1, ranks2):
        n = len(ranks1)
        diff_sum = sum((ranks1[i] - ranks2[i]) ** 2 for i in range(n))
        rho_numerator = 1 - (6 * diff_sum) / (n * (n**2 - 1))
        return rho_numerator
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        phi_f = characteristic_polynomial(f)
        omega_phi_f = adjoint_group_order(phi_f)
        e_f = circuit_entanglement_complexity(f)
        
        if omega_phi_f is None or e_f == 0:
            continue
        
        results.append((omega_phi_f, e_f))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    omega_ranks = sorted(range(len(results)), key=lambda i: results[i][0])
    e_ranks = sorted(range(len(results)), key=lambda i: results[i][1])
    
    rho = spearman_correlation(omega_ranks, e_ranks)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(rho) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        std_rho = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")