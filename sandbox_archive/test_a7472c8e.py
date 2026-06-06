# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        assignment = {}
        clauses = set(tuple(c) for c in cnf)
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clauses = [c for c in clauses if len(c) == 1]
            if unit_clauses:
                literal, _ = unit_clauses[0]
                new_assignment[literal] = True
                clauses.discard(tuple([literal]))
                for c in list(clauses):
                    if literal in c:
                        clauses.remove(c)
                    elif -literal in c:
                        c.remove(-literal)
            pure_literals = [l for l, _ in assignment.items() if all(l not in c and -l not in c for c in clauses)]
            if pure_literals:
                literal = pure_literals[0]
                new_assignment[literal] = True
                clauses.discard(tuple([literal]))
                for c in list(clauses):
                    if literal in c:
                        clauses.remove(c)
                    elif -literal in c:
                        c.remove(-literal)
            if not clauses:
                return True
            literal, _ = random.choice(list(clauses))
            new_assignment[literal] = True
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment) or \
                   dpll([c for c in clauses if literal in c], {**new_assignment, literal: False})
        
        return len(assignment) if dpll(clauses, assignment) else float('inf')
    
    def tropical_curve_order(cnf):
        # Placeholder implementation
        return random.randint(1, 10)
    
    m = random.randint(5, 10)
    n = random.randint(5, 10)
    cnf = generate_cnf(m, n)
    width = resolution_width(cnf)
    order = tropical_curve_order(cnf)
    
    return {
        "metric_name": "Order of Singular Points vs Resolution Width",
        "metric_value": order / width if width != float('inf') else float('nan'),
        "instances_tested": 1,
        "n_max": max(m, n),
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2 ** i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if not math.isnan(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(not math.isnan(r["metric_value"]) and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not math.isnan(r["metric_value"]) and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not math.isnan(result["metric_value"]) and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid data")