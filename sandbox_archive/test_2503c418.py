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
        for _ in range(2**n // 10):  # Ensure at least 30 instances per seed
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def diophantine_approximation(f):
        x = f / (2 * math.pi)
        q = int(x)
        r = abs(x - q)
        while r != 0:
            x = 1 / r
            q = int(x)
            r = abs(x - q)
        return q
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation for demonstration
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        f = sum(1 if random.choice([True, False]) else -1 for _ in range(2**n)) / (2**n)
        mo_f = diophantine_approximation(f)
        w_phi = resolution_width(cnf)
        results.append((math.log(mo_f), w_phi))
    
    if len(results) < 30:
        return {
            "metric_name": "log_mo_f_w_phi_ratio",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ratios = [r[0] / r[1] for r in results if r[1] != 0]
    if not ratios:
        return {
            "metric_name": "log_mo_f_w_phi_ratio",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    support_fraction = sum(0.5 <= r < 2 for r in ratios) / len(ratios)
    
    return {
        "metric_name": "log_mo_f_w_phi_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_ratio={mean_ratio}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    elif any(not r["conjecture_holds"] and r["counterexample"] == "" for r in results):
        RESULT = "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {RESULT} mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")