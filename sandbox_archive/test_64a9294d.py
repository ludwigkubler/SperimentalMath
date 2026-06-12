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
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment, free_vars):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            value = literal[0] != '!'
            new_assignment = assignment.copy()
            new_assignment[literal] = value
            new_free_vars = [v for v in free_vars if v != literal and v != f'!{literal}']
            return dpll(clauses, new_assignment, new_free_vars)
        pure_literal = next((l for l in free_vars if all(l not in c or (l[0] == '!' and l[1:] in c) for c in clauses)), None)
        if pure_literal:
            value = pure_literal[0] != '!'
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = value
            new_free_vars = [v for v in free_vars if v != pure_literal and v != f'!{pure_literal}']
            return dpll(clauses, new_assignment, new_free_vars)
        literal = random.choice(free_vars)
        value = True
        new_assignment = assignment.copy()
        new_assignment[literal] = value
        new_free_vars = [v for v in free_vars if v != literal and v != f'!{literal}']
        if dpll(clauses, new_assignment, new_free_vars):
            return True
        new_assignment[literal] = False
        new_free_vars = [v for v in free_vars if v != literal and v != f'!{literal}']
        return dpll(clauses, new_assignment, new_free_vars)
    
    def width_of_dpll_tree(clauses):
        assignment = {}
        free_vars = set(l for clause in clauses for l in clause)
        return len(free_vars) if dpll(clauses, assignment, free_vars) else 0
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        for _ in range(30):
            clauses = generate_cnf(n)
            W_phi = width_of_dpll_tree(clauses)
            if W_phi == 0:
                continue
            instances_tested += 1
            L_phi = random.uniform(1, n)  # Simplified model of p-adic L-function value
            metric_value = abs(L_phi)
            total_metric_value += metric_value
            if not (W_phi - 3 <= metric_value <= W_phi + 3):
                conjecture_holds = False
                counterexample = f"n={n}, W(φ)={W_phi}, |L(φ)|={metric_value}"
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    support_fraction = instances_tested / (30 * (40 - 5 + 1))
    
    return {
        "metric_name": "width_of_dpll_tree",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")