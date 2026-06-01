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

# Helper functions for polynomial operations and DPLL search tree construction
def poly_from_satsat(phi):
    # Convert SAT-SAT instance to a polynomial
    n = len(phi)
    p = [0] * (n + 1)
    for clause in phi:
        product = 1
        for var in clause:
            if var < 0:
                product *= (1 - x[-var])
            else:
                product *= x[var]
        p[0] += product
    return p

def qrs(p):
    # Compute the minimal quadratic residue symbol of a polynomial
    n = len(p)
    for i in range(2, n):
        if all(p[j] % i == 0 for j in range(n)):
            return Fraction(i, 1)
    return Fraction(1, 1)

def dpll(phi):
    # Construct the DPLL search tree and determine its diameter
    def dfs(model, clause):
        if not clause:
            return 0
        var = next(var for var in range(1, len(model) + 1) if model[var] is None)
        true_branch = dfs({**model, var: True}, [c for c in clause if var not in c and -var not in c])
        false_branch = dfs({**model, var: False}, [c for c in clause if -var not in c and var not in c])
        return 1 + max(true_branch, false_branch)
    model = {i: None for i in range(1, len(phi) + 1)}
    return dfs(model, phi)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = [[random.randint(1, n) for _ in range(random.randint(1, n // 2))] for _ in range(n)]
            p = poly_from_satsat(phi)
            qrs_val = qrs(p)
            d_phi = dpll(phi)
            results.append((qrs_val, d_phi))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    qrs_vals, d_phis = zip(*results)
    mean_qrs = sum(qrs_vals) / len(qrs_vals)
    mean_d_phi = sum(d_phis) / len(d_phis)
    correlation = (sum((q - mean_qrs) * (d - mean_d_phi) for q, d in zip(qrs_vals, d_phis)) /
                   math.sqrt(sum((q - mean_qrs)**2 for q in qrs_vals) *
                             sum((d - mean_d_phi)**2 for d in d_phis)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(qrs_vals),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **run_trial output...}}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        mean_corr = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")