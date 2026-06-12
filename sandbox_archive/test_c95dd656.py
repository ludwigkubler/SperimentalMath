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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) for _ in range(random.randint(2, 3))]
        cnf.append(clause)
    return cnf

def resolution_width(cnf):
    unit_clauses = set()
    while True:
        new_unit_clauses = []
        for clause in cnf:
            if len(clause) == 1:
                lit = clause[0]
                if -lit not in unit_clauses:
                    unit_clauses.add(lit)
                    new_unit_clauses.extend([c for c in cnf if lit in c or -lit in c])
        if not new_unit_clauses:
            break
        cnf.extend(new_unit_clauses)
    return len(unit_clauses)

def p_adic_divergence(poly, p):
    n = len(poly)
    k = 0
    while True:
        if all(x % p == 0 for x in poly):
            k += 1
            poly = [x // p for x in poly]
        else:
            return k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, 2 * n)
        resolution_width_value = resolution_width(cnf)
        poly = [sum(1 << (abs(lit) - 1) if lit > 0 else -(1 << (abs(lit) - 1)) for lit in clause) for clause in cnf]
        p_adic_divergence_value = p_adic_divergence(poly, 2)
        
        results.append({
            "n": n,
            "resolution_width": resolution_width_value,
            "p_adic_divergence": p_adic_divergence_value
        })
    
    k_values = [result["p_adic_divergence"] for result in results]
    w_values = [result["resolution_width"] for result in results]
    
    if len(k_values) < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(k_values),
            "n_max": max(results, key=lambda x: x["n"])["n"],
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_k = sum(k_values) / len(k_values)
    mean_w = sum(w_values) / len(w_values)
    variance_k = sum((x - mean_k) ** 2 for x in k_values) / len(k_values)
    variance_w = sum((x - mean_w) ** 2 for x in w_values) / len(w_values)
    
    covariance_kw = sum((k_values[i] - mean_k) * (w_values[i] - mean_w) for i in range(len(k_values))) / len(k_values)
    
    pearson_corr = covariance_kw / math.sqrt(variance_k * variance_w)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_corr,
        "instances_tested": len(k_values),
        "n_max": max(results, key=lambda x: x["n"])["n"],
        "conjecture_holds": pearson_corr >= 0.7 and min(pearson_corr for _ in range(len(k_values))) >= 0.5,
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
    
    mean_corr = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] >= 0.7 and min(result["metric_value"] for _ in range(len(k_values))) >= 0.5 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")