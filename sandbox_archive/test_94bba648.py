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
    
    def poly_from_satsat(phi):
        n = len(phi)
        poly = 0
        for clause in phi:
            term = 1
            for var in clause:
                if var < 0:
                    term &= (1 - x[-var])
                else:
                    term &= x[var]
            poly |= term
        return poly
    
    def qrs(poly):
        n = len(bin(poly)) - 2
        a = random.randint(1, n-1)
        while math.gcd(a, n) != 1:
            a = random.randint(1, n-1)
        return pow(a, (n-1)//2, n)
    
    def dpll(phi):
        if not phi:
            return 0
        for clause in phi:
            if not any(var in clause for var in range(1, len(phi)+1)):
                return float('inf')
        unit_clauses = [var for var in range(1, len(phi)+1) if any(var in clause for clause in phi)]
        if unit_clauses:
            phi = [clause for clause in phi if not any(var in clause for var in unit_clauses)]
            return 1 + min(dpll(phi), dpll([[var] for var in range(1, len(phi)+1) if var not in unit_clauses]))
        p_var = random.choice(range(1, len(phi)+1))
        phi_true = [clause for clause in phi if p_var in clause]
        phi_false = [clause for clause in phi if -p_var in clause]
        return 1 + min(dpll(phi_true), dpll(phi_false))
    
    def generate_phi(n):
        phi = []
        for _ in range(2**n):
            clause = random.sample(range(1, n+1), random.randint(1, n))
            if all(var not in phi[-1] for var in clause):
                phi.append(clause)
        return phi
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_phi(n)
        poly = poly_from_satsat(phi)
        qrs_value = qrs(poly)
        dpll_diameter = dpll(phi)
        results.append({"n": n, "qrs": qrs_value, "dpll_diameter": dpll_diameter})
    
    if not results:
        return {
            "metric_name": "qrs_dpll_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    qrs_values = [result["qrs"] for result in results]
    dpll_diameters = [result["dpll_diameter"] for result in results]
    
    mean_qrs = sum(qrs_values) / len(qrs_values)
    mean_dpll = sum(dpll_diameters) / len(dpll_diameters)
    correlation = sum((qrs - mean_qrs) * (d - mean_dpll) for qrs, d in zip(qrs_values, dpll_diameters)) / (len(results) * math.sqrt(sum((qrs - mean_qrs)**2 for qrs in qrs_values) * sum((d - mean_dpll)**2 for d in dpll_diameters)))
    
    return {
        "metric_name": "qrs_dpll_correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.5) / len(results)
    
    if all(abs(result["metric_value"]) >= 0.5 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")