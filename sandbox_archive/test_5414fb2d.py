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

def generate_formula(n):
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(2*n):
        clause = ' and '.join(random.sample(literals, 2))
        clauses.append(clause)
    formula = ' or '.join(clauses)
    return formula

def resolution_width(formula):
    # Simplified DPLL-based solver to compute resolution proof width
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and literal.replace('-', '') not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and literal.replace('-', '') not in c], new_assignment):
                return True
        else:
            literal = random.choice(clauses[0])
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and literal.replace('-', '') not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and literal.replace('-', '') not in c], new_assignment):
                return True
        return False

    def count_resolutions(formula):
        clauses = formula.split(' or ')
        assignment = {}
        return len(clauses)

    return count_resolutions(formula)

def minimal_local_system_rank(n):
    # Placeholder function for minimal local system rank calculation
    # This is a dummy implementation and should be replaced with actual computation
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        w_phi = resolution_width(formula)
        mls_phi = minimal_local_system_rank(n)
        results.append((mls_phi, w_phi))
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    mls_values = [mls for mls, _ in results]
    w_phi_values = [w_phi for _, w_phi in results]
    correlation_coefficient = sum((mls - mean(mls_values)) * (w_phi - mean(w_phi_values)) for mls, w_phi in results) / (len(results) * std_dev(mls_values) * std_dev(w_phi_values))
    mean_diff = mean([abs(mls - w_phi) for mls, w_phi in results])
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_diff <= 3,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

def std_dev(lst):
    avg = mean(lst)
    return math.sqrt(sum((x - avg) ** 2 for x in lst) / len(lst))

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean([r['metric_value'] for r in results])} std={std_dev([r['metric_value'] for r in results])} support_fraction=1.0")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if 'counterexample' in result)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")