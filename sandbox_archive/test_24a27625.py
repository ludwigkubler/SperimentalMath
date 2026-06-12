# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def generate_cnf(n):
    clauses = []
    for _ in range(n * (n - 1) // 2):
        literals = [random.randint(1, n), random.randint(-n, -1)]
        random.shuffle(literals)
        clauses.append(tuple(literals))
    return clauses

def dpll(cnf):
    def solve(model):
        if not cnf:
            return model
        unit_clauses = [c for c in cnf if len(c) == 1]
        if not unit_clauses:
            return None
        literal, _ = unit_clauses[0]
        new_model = model.copy()
        new_model[literal] = True
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        result = solve(new_model)
        if result is not None:
            return result
        new_model[literal] = False
        new_model[-literal] = True
        new_cnf = [c for c in cnf if -literal not in c and literal not in c]
        return solve(new_model)

    model = {}
    return solve(model)

def compute_qmc_order(n, epsilon):
    # Simplified approximation of the minimal order of QMC points
    return int(math.ceil(2 * n * math.log(1 / epsilon)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        w_phi = len(dpll(cnf)) if dpll(cnf) is not None else float('inf')
        qmc_order = compute_qmc_order(n, 1/1000)
        
        results.append({
            "n": n,
            "w_phi": w_phi,
            "qmc_order": qmc_order
        })
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    w_phi_values = [r["w_phi"] for r in results]
    qmc_order_values = [r["qmc_order"] for r in results]
    
    mean_w_phi = sum(w_phi_values) / len(w_phi_values)
    mean_qmc_order = sum(qmc_order_values) / len(qmc_order_values)
    
    correlation_coefficient = sum((w - mean_w_phi) * (q - mean_qmc_order) for w, q in zip(w_phi_values, qmc_order_values)) / \
                             math.sqrt(sum((w - mean_w_phi)**2 for w in w_phi_values) * sum((q - mean_qmc_order)**2 for q in qmc_order_values))
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_not_sufficiently_high\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_or_budget_exceeded n_tested=30")