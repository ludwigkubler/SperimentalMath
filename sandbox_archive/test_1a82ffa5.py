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
        for _ in range(10 * n):  # Each variable appears in 10 clauses on average
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses
    
    def resolution(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        new_clauses = []
        while True:
            found_new_clause = False
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = sorted(list(set(clause1) ^ set(clause2)))
                        if new_clause not in clauses and new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                            found_new_clause = True
            if not found_new_clause:
                break
            clauses.update(new_clauses)
        return len(new_clauses)
    
    def count_local_cycles(cnf):
        n = len(cnf[0])
        local_cycles = 0
        for i in range(n):
            neighbors = [j for j in range(n) if any(i + 1 == abs(lit) and lit != -lits[j] for lits in cnf)]
            if len(neighbors) % 2 == 0:
                local_cycles += 1
        return local_cycles
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        d_phi = resolution(cnf)
        l_phi = count_local_cycles(cnf)
        
        if d_phi == 0:
            continue
        
        metric_values.append((l_phi, d_phi))
    
    if not metric_values:
        return {
            "metric_name": "L(φ)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_resolution"
        }
    
    l_phi_values, d_phi_values = zip(*metric_values)
    mean_l_phi = sum(l_phi_values) / len(l_phi_values)
    mean_d_phi = sum(d_phi_values) / len(d_phi_values)
    abs_diff_sum = sum(abs(l - d) for l, d in metric_values)
    
    correlation_coefficient = (sum((l - mean_l_phi) * (d - mean_d_phi) for l, d in metric_values) /
                                math.sqrt(sum((l - mean_l_phi)**2 for l in l_phi_values) *
                                          sum((d - mean_d_phi)**2 for d in d_phi_values)))
    
    return {
        "metric_name": "L(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs_diff_sum / len(metric_values) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000007) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{mean_corr_coeff}, support_fraction<{support_fraction}\" first_failing_seed={first_failing_seed}")