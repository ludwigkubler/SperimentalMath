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
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def compute_fsi(cnf):
        n = len(cnf[0])
        fsi = 0
        for clause in cnf:
            sign_product = 1
            for literal in clause:
                sign_product *= literal
            fsi += sign_product
        return abs(fsi) / (2**n)
    
    def compute_ec(cnf):
        n = len(cnf[0])
        ec = 0
        for i in range(n):
            for j in range(i + 1, n):
                if any(lit * other_lit < 0 for lit, other_lit in zip(cnf[i], cnf[j])):
                    ec += 1
        return ec
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            fsi = compute_fsi(cnf)
            ec = compute_ec(cnf)
            results.append((fsi, ec))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    fsi_values = [fsi for fsi, ec in results]
    ec_values = [ec for fsi, ec in results]
    
    mean_fsi = sum(fsi_values) / len(fsi_values)
    mean_ec = sum(ec_values) / len(ec_values)
    
    correlation = 0
    for fsi, ec in results:
        correlation += (fsi - mean_fsi) * (ec - mean_ec)
    correlation /= math.sqrt(sum((fsi - mean_fsi)**2 for fsi in fsi_values)) * math.sqrt(sum((ec - mean_ec)**2 for ec in ec_values))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        mean_correlation = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.8) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=NA support_fraction={support_fraction}")