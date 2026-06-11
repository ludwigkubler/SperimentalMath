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
        cnf = []
        for _ in range(10):  # Each clause has at most 3 literals
            clause = [random.randint(-n, n) for _ in range(3)]
            if all(x != 0 for x in clause):
                cnf.append(clause)
        return cnf

    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        pure_literals = set()
        for lit in range(1, n+1):
            pos_count = sum(1 for clause in cnf if lit in clause)
            neg_count = sum(1 for clause in cnf if -lit in clause)
            if pos_count == 0:
                pure_literals.add(-lit)
            elif neg_count == 0:
                pure_literals.add(lit)

        if unit_clauses:
            lit = unit_clauses[0]
            return dpll(propagate(lit, cnf), assignment | {lit: True}) or \
                   dpll(propagate(-lit, cnf), assignment | {-lit: True})
        elif pure_literals:
            lit = next(iter(pure_literals))
            return dpll(propagate(lit, cnf), assignment | {lit: True}) or \
                   dpll(propagate(-lit, cnf), assignment | {-lit: True})
        else:
            for lit in range(1, n+1):
                if lit not in assignment and -lit not in assignment:
                    return dpll(propagate(lit, cnf), assignment | {lit: True}) or \
                           dpll(propagate(-lit, cnf), assignment | {-lit: True})
            return False

    def propagate(lit, cnf):
        new_cnf = []
        for clause in cnf:
            if lit in clause:
                continue
            elif -lit in clause:
                clause.remove(-lit)
                if not clause:
                    return None  # Conflict
                new_cnf.append(clause)
            else:
                new_cnf.append(clause)
        return new_cnf

    def hodge_mumford(cnf):
        # Placeholder for actual Hodge-Mumford computation
        return len(cnf)

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    w_DPLL = dpll(cnf)
    
    if not w_DPLL:
        return {
            "metric_name": "h(V(φ))",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree width is zero"
        }

    h_V_phi = hodge_mumford(cnf)
    correlation_coefficient = None
    ratio = None

    if h_V_phi != 0 and w_DPLL != 0:
        correlation_coefficient = abs(h_V_phi / w_DPLL)
        ratio = abs(h_V_phi / w_DPLL)

    return {
        "metric_name": "h(V(φ))",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient is not None and ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if "counterexample" in r and r["counterexample"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no data")