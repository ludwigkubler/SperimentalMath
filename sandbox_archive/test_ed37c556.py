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
        for _ in range(10 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(2, 4))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        unsatisfied = [c for c in cnf if not any(l in assignment and assignment[l] == True for l in c)]
        if not unsatisfied:
            return assignment
        unit_clauses = [c for c in unsatisfied if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True if literal > 0 else False
            return dpll(cnf, new_assignment)
        pure_literals = {}
        for c in unsatisfied:
            for l in c:
                if abs(l) not in pure_literals:
                    pure_literals[abs(l)] = (l > 0, 1)
                elif pure_literals[abs(l)][0] != (l > 0):
                    pure_literals[abs(l)][1] += 1
        pure_clauses = [c for c in unsatisfied if any(abs(l) in pure_literals and pure_literals[abs(l)][1] == len(c) for l in c)]
        if pure_clauses:
            literal, polarity = next((l, p) for l, (p, count) in pure_literals.items() if count == len(pure_clauses))
            new_assignment = assignment.copy()
            new_assignment[literal] = polarity
            return dpll(cnf, new_assignment)
        return None
    
    def resolution(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    common_literals = [l for l in clauses[i] if -l in clauses[j]]
                    if common_literals:
                        new_clause = list(set([l for l in clauses[i] if l not in common_literals] + [l for l in clauses[j] if l not in common_literals]))
                        new_clauses.append(new_clause)
            if new_clauses == []:
                return len(clauses)
            clauses += new_clauses
    
    def normal_form(cnf):
        assignment = dpll(cnf)
        if assignment is None:
            return []
        return [tuple(sorted([l for l in cnf[i] if assignment[l] == True])) for i in range(len(cnf))]
    
    def coxeter_group_order(n):
        # Simplified Coxeter group order approximation
        return math.factorial(n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    nf = normal_form(cnf)
    w = resolution(cnf)
    if w == 0:
        return {
            "metric_name": "Ratio |N(φ)| / w(φ)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Resolution proof width is zero"
        }
    ratio = len(nf) / w
    return {
        "metric_name": "Ratio |N(φ)| / w(φ)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= coxeter_group_order(n) else False,
        "counterexample": "" if ratio <= coxeter_group_order(n) else "Ratio exceeds Coxeter group order"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds Coxeter group order\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")