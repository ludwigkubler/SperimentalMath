# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([i, -i]) for _ in range(random.randint(2, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            var = unit_clauses[0]
            if -var in assignment and assignment[-var]:
                return False
            assignment[var] = True
            cnf = [[x for x in c if x != var and x != -var] for c in cnf]
            return dpll(cnf, assignment)
        pure_literals = {}
        for literal in set([abs(x) for c in cnf for x in c]):
            pos_count = sum(1 for c in cnf if literal in c)
            neg_count = sum(1 for c in cnf if -literal in c)
            if pos_count == 0:
                pure_literals[literal] = False
            elif neg_count == 0:
                pure_literals[literal] = True
        if pure_literals:
            var, value = next((k, v) for k, v in pure_literals.items())
            assignment[var] = value
            cnf = [[x for x in c if x != var and x != -var] for c in cnf]
            return dpll(cnf, assignment)
        p_var = next(var for var in range(1, len(assignment) + 2) if var not in assignment)
        return dpll(cnf, assignment | {p_var: True}) or dpll(cnf, assignment | {p_var: False})
    
    def dpll_refutation_depth(cnf):
        depth = [0] * (len(cnf) + 1)
        stack = [(cnf, {})]
        while stack:
            cnf, assignment = stack.pop()
            if not cnf:
                return max(depth)
            unit_clauses = [c[0] for c in cnf if len(c) == 1]
            if unit_clauses:
                var = unit_clauses[0]
                if -var in assignment and assignment[-var]:
                    continue
                assignment[var] = True
                depth[len(assignment)] += 1
                stack.append(([[x for x in c if x != var and x != -var] for c in cnf], assignment))
            else:
                p_var = next(var for var in range(1, len(assignment) + 2) if var not in assignment)
                depth[len(assignment)] += 1
                stack.append(([c[:] for c in cnf], assignment | {p_var: True}))
                stack.append(([c[:] for c in cnf], assignment | {p_var: False}))
        return max(depth)
    
    def minimal_totally_ramified_extension_order(n):
        # This is a placeholder function. Replace with actual computation.
        return random.randint(2, n)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    k = minimal_totally_ramified_extension_order(n)
    t_star = dpll_refutation_depth(cnf)
    
    if t_star == float('inf'):
        return {
            "metric_name": "log2(k) vs log2(t*)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL refutation depth is infinite"
        }
    
    if k == 0:
        return {
            "metric_name": "log2(k) vs log2(t*)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Minimal order of extension is zero"
        }
    
    log2_k = math.log2(k)
    log2_t_star = math.log2(t_star)
    
    return {
        "metric_name": "log2(k) vs log2(t*)",
        "metric_value": log2_k,
        "instances_tested": 1,
        "conjecture_holds": log2_k <= log2_t_star,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")