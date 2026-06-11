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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(cnf):
        # Simplified SAT solver using backtracking
        assignment = {}
        def backtrack():
            if all(any(l in assignment and assignment[l] == (l > 0) for l in clause) for clause in cnf):
                return True
            var = next((v for v in range(1, n + 1) if v not in assignment), None)
            if var is None:
                return False
            for val in [True, False]:
                assignment[var] = val
                if backtrack():
                    return True
                del assignment[var]
            return False
        return backtrack()
    
    def p_adic_valuation(cnf):
        # Simplified p-adic valuation calculation (placeholder)
        return random.random() * n
    
    def complexity_of_distinguishing(phi, phi_prime):
        # Simplified complexity measure (placeholder)
        return len(phi) + len(phi_prime)
    
    results = []
    for _ in range(30):
        n = 5 + (random.randint(1, 4) * 5)
        phi = generate_cnf(n)
        phi_prime = [clause[:] for clause in phi]
        
        if not is_satisfiable(phi):
            continue
        
        ord_p_val = p_adic_valuation(phi)
        comp_complexity = complexity_of_distinguishing(phi, phi_prime)
        
        results.append({
            "n": n,
            "ord_p_val": ord_p_val,
            "comp_complexity": comp_complexity
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No satisfiable CNFs generated"
        }
    
    ord_p_vals = [r["ord_p_val"] for r in results]
    comp_complexities = [r["comp_complexity"] for r in results]
    
    mean_ord_p = sum(ord_p_vals) / len(ord_p_vals)
    mean_comp_complexity = sum(comp_complexities) / len(comp_complexities)
    
    correlation_coefficient = (sum((ord_p - mean_ord_p) * (comp - mean_comp_complexity) for ord_p, comp in zip(ord_p_vals, comp_complexities)) /
                               math.sqrt(sum((ord_p - mean_ord_p) ** 2 for ord_p in ord_p_vals) *
                                         sum((comp - mean_comp_complexity) ** 2 for comp in comp_complexities)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_comp_complexity <= 3.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample_desc = f"Seed {first_failing_seed} failed the conjecture"
        result = "FALSIFIED"
    else:
        result = "INCONCLUSIVE"
    
    print(f"RESULT: {result} mean={mean_metric_value} std={math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results)) if 'mean_metric_value' in locals() else None} support_fraction={support_fraction}")