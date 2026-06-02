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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}, model=[]):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(cnf[0]) + 1) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[literal] = value
            if dpll(cnf, new_assignment, model):
                return True
        return False
    
    def eta_quotient(cnf):
        # Placeholder implementation. This is a dummy function.
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        eta_phi = eta_quotient(cnf)
        d_phi = dpll(cnf)
        
        if not d_phi:
            return {
                "metric_name": "eta_phi",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL solver failed to find a model"
            }
        
        results.append((eta_phi, d_phi))
    
    if len(results) < 30:
        return {
            "metric_name": "eta_phi",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    eta_phis, d_phis = zip(*results)
    mean_eta_phi = sum(eta_phis) / len(eta_phis)
    mean_d_phi = sum(d_phis) / len(d_phis)
    
    correlation_coefficient = 0
    for i in range(len(eta_phis)):
        correlation_coefficient += (eta_phis[i] - mean_eta_phi) * (d_phis[i] - mean_d_phi)
    correlation_coefficient /= math.sqrt(sum((x - mean_eta_phi) ** 2 for x in eta_phis)) * math.sqrt(sum((y - mean_d_phi) ** 2 for y in d_phis))
    
    return {
        "metric_name": "eta_phi",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Insufficient data to determine"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")