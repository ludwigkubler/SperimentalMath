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

def generate_kcnf(n, k):
    clauses = []
    for _ in range(k):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)
                  for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def resolution_width(phi):
    # Simplified DPLL algorithm to estimate resolution width
    def dpll(clauses, assignment):
        if not clauses:
            return len(assignment)
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is None:
            literal = random.choice([l for clause in clauses for l in clause])
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll(clauses, new_assignment)
        literal = unit_clause[0]
        if literal in assignment and assignment[literal]:
            return float('inf')
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        new_clauses = [[-l for l in clause] if l == -literal else clause for clause in new_clauses]
        return min(dpll(new_clauses, assignment), dpll(new_clauses, {**assignment, literal: False}))
    
    return dpll(phi, {})

def hodge_index(n):
    # Simplified Hodge index calculation (placeholder)
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            k = random.randint(1, min(n-1, 10))
            phi = generate_kcnf(n, k)
            w_phi = resolution_width(phi)
            H_phi = hodge_index(n)
            if w_phi == float('inf'):
                continue
            results.append((n, w_phi, H_phi))
    
    total_w_phi = sum(w for _, w, _ in results)
    total_H_phi = sum(H for _, _, H in results)
    n_max = max(n for n, _, _ in results)
    conjecture_holds = all(log2(n**(k+1)) <= w + H for n, w, H in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": total_w_phi / len(results),
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def log2(x):
    return math.log(x, 2)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_w_phi = sum(result["metric_value"] for result in results) / len(results)
    std_w_phi = math.sqrt(sum((result["metric_value"] - mean_w_phi)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_w_phi} std={std_w_phi} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")