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

def generate_cnf(n):
    clauses = []
    for _ in range(n * (n + 1) // 2):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        clauses.append(clause)
    return clauses

def dpll(cnf):
    def solve(model):
        if not cnf:
            return model
        literal = next(l for l in range(1, n + 1) if l not in model and -l not in model)
        new_model = model.copy()
        new_model[literal] = True
        if solve(new_model):
            return new_model
        new_model[literal] = False
        if solve(new_model):
            return new_model
        return None

    n = len(cnf[0])
    model = {}
    result = solve(model)
    if result:
        return max(len([l for l in model if model[l]]) for l in range(1, n + 1))
    else:
        return float('inf')

def zeta_function(cnf):
    def evaluate_clause(clause, assignment):
        return any(assignment[abs(l) - 1] == (l > 0) for l in clause)

    def evaluate_formula(formula, assignment):
        return all(evaluate_clause(clause, assignment) for clause in formula)

    n = len(cnf[0])
    count = 0
    total = 2 ** n
    while count < total:
        assignment = {i: bool(random.getrandbits(1)) for i in range(n)}
        if evaluate_formula(cnf, assignment):
            count += 1
    return Fraction(count, total)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        zeta_order = math.log(zeta_function(cnf), 2)
        proof_width = dpll(cnf)
        
        if proof_width == float('inf'):
            return {
                "metric_name": "Order(ζφ)",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "DPLL solver timed out"
            }
        
        results.append((zeta_order, proof_width))
    
    if len(results) < 30:
        return {
            "metric_name": "Order(ζφ)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    zeta_orders = [r[0] for r in results]
    proof_widths = [r[1] for r in results]
    correlation = sum((z - mean_z) * (w - mean_w) for z, w in zip(zeta_orders, proof_widths)) / len(results)
    mean_z = sum(zeta_orders) / len(zeta_orders)
    mean_w = sum(proof_widths) / len(proof_widths)
    
    return {
        "metric_name": "Order(ζφ)",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(r is not None for r in results):
        mean = sum(results) / len(results)
        std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if abs(r) >= 0.7) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = seeds[results.index(next(r for r in results if abs(r) < 0.7))]
            print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_failed")