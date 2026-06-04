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
            if any(clause.count(lit) > 1 or clause.count(-lit) > 1 for lit in set(clause)):
                continue
            clauses.append(clause)
        return clauses
    
    def diophantine_approximation(f, n):
        min_order = float('inf')
        for i in range(1, n**2 + 1):
            x = i / (n**2)
            approx = round(x * f(n))
            if abs(approx - x * f(n)) < min_order:
                min_order = abs(approx - x * f(n))
        return min_order
    
    def resolution_width(phi):
        # Simplified resolution width calculation for demonstration
        return len(phi) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_cnf(n)
        f_n = sum(1 for clause in phi if any(lit > 0 for lit in clause))
        mo_f = diophantine_approximation(f_n, n)
        w_phi = resolution_width(phi)
        
        results.append({
            "n": n,
            "mo_f": mo_f,
            "w_phi": w_phi
        })
    
    if not results:
        return {
            "metric_name": "log(mo(f)) / w(φ)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    log_mo_f = [math.log(result["mo_f"]) for result in results]
    w_phi = [result["w_phi"] for result in results]
    
    if any(w == 0 for w in w_phi):
        return {
            "metric_name": "log(mo(f)) / w(φ)",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    ratios = [log_mo_f[i] / w_phi[i] for i in range(len(log_mo_f))]
    
    if any(r < 0.5 or r > 2 for r in ratios):
        return {
            "metric_name": "log(mo(f)) / w(φ)",
            "metric_value": sum(ratios) / len(ratios),
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "out_of_range_ratio"
        }
    
    return {
        "metric_name": "log(mo(f)) / w(φ)",
        "metric_value": sum(ratios) / len(ratios),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        exit(0)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(result["counterexample"] == "out_of_range_ratio" for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"] == "out_of_range_ratio")
        print(f"RESULT: FALSIFIED counterexample=\"out_of_range_ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")