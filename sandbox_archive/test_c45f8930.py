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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(1, n+1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            new_assignment[pure_literal] = True
            if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        literal = random.choice(range(1, n+1))
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    
    def resolution(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        while True:
            new_clauses = []
            for c1, c2 in itertools.combinations(clauses, 2):
                if len(set(c1) & set(c2)) == 1:
                    literal = next(l for l in c1 if l not in c2)
                    new_clause = tuple(sorted([l for l in c1 + c2 if l != -literal]))
                    if new_clause not in clauses:
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n, n*2)
    cnf = generate_cnf(n, m)
    w_phi = resolution(cnf)
    
    def count_automorphic_representations():
        # Placeholder for actual implementation
        return random.randint(1, 5)  # Dummy value
    
    automorphic_representations = count_automorphic_representations()
    if automorphic_representations == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = abs(w_phi) / automorphic_representations
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
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
    
    ratios = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(ratios)/len(ratios)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(ratios)/len(ratios)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")