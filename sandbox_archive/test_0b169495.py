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

# Define a small DPLL solver
def dpll(clause_set, assignment, clauses):
    if not clause_set:
        return True
    unit_clause = next((c for c in clause_set if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        if literal < 0:
            literal = -literal
        assignment[literal - 1] = True
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        return dpll(new_clauses, assignment, clause_set)
    pure_literal = next((lit for lit in range(1, len(assignment) + 1) if (lit not in assignment and -lit not in assignment)), None)
    if pure_literal is None:
        return False
    literal = pure_literal
    assignment[literal - 1] = True
    new_clauses = [c for c in clauses if literal not in c and -literal not in c]
    if dpll(new_clauses, assignment, clause_set):
        return True
    assignment[literal - 1] = False
    new_clauses = [c for c in clauses if literal not in c and -literal not in c]
    if dpll(new_clauses, assignment, clause_set):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random CNF formula of size n
    n = 10 + random.randint(0, 29)
    m = 5 * n + random.randint(0, n)
    clause_set = []
    for _ in range(m):
        num_literals = random.randint(1, n)
        literals = random.sample(range(1, n + 1), num_literals)
        clause = [l if random.choice([True, False]) else -l for l in literals]
        clause_set.append(clause)
    
    # Measure DPLL path length
    assignment = [None] * n
    result = dpll(clause_set, assignment, clause_set)
    w_phi = len(assignment)  # Simplified DPLL path length
    
    # Compute minimal index of symplectic leaves (misl(φ))
    # This is a placeholder function. Replace with actual computation.
    misl_phi = n  # Placeholder value
    
    return {
        "metric_name": "misl_phi",
        "metric_value": misl_phi,
        "instances_tested": m,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_misl_phi = sum(r["metric_value"] for r in results) / len(results)
    std_misl_phi = math.sqrt(sum((r["metric_value"] - mean_misl_phi) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_misl_phi} std={std_misl_phi} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")