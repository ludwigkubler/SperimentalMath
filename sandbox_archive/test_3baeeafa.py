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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def p_adic_valuation(cnf):
        valuation = 0
        for clause in cnf:
            for literal in clause:
                if abs(literal) % 2 == 0:
                    valuation += 1
        return valuation

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        unsatisfiable_cnf = [[-x for x in clause] for clause in cnf]
        
        p_val_cnf = p_adic_valuation(cnf)
        p_val_unsat_cnf = p_adic_valuation(unsatisfiable_cnf)
        
        if p_val_cnf == 0 or p_val_unsat_cnf == 0:
            continue
        
        results.append({
            "n": n,
            "p_val_cnf": p_val_cnf,
            "p_val_unsat_cnf": p_val_unsat_cnf
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    p_vals_cnf = [r["p_val_cnf"] for r in results]
    p_vals_unsat_cnf = [r["p_val_unsat_cnf"] for r in results]
    
    mean_p_val_cnf = sum(p_vals_cnf) / len(p_vals_cnf)
    mean_p_val_unsat_cnf = sum(p_vals_unsat_cnf) / len(p_vals_unsat_cnf)
    
    covariance = sum((p_vals_cnf[i] - mean_p_val_cnf) * (p_vals_unsat_cnf[i] - mean_p_val_unsat_cnf) for i in range(len(p_vals_cnf)))
    variance_cnf = sum((p_vals_cnf[i] - mean_p_val_cnf) ** 2 for i in range(len(p_vals_cnf)))
    variance_unsat_cnf = sum((p_vals_unsat_cnf[i] - mean_p_val_unsat_cnf) ** 2 for i in range(len(p_vals_unsat_cnf)))
    
    if variance_cnf == 0 or variance_unsat_cnf == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "Zero variance in p-adic valuation"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_cnf) * math.sqrt(variance_unsat_cnf))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": False if pearson_corr < 0.8 else True,
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
    
    if not all(r["conjecture_holds"] for r in results):
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")