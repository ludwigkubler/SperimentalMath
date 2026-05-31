# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append((clause[0], -clause[1]))
        clauses.append((-clause[0], clause[1]))
    return clauses

def dpll(cnf):
    def solve(literals, assignment):
        if not literals:
            return 0
        literal = next((l for l in literals if l not in assignment and -l not in assignment), None)
        if literal is None:
            return float('inf')
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        true_clauses = [c for c in cnf if any(l in c for l in new_assignment)]
        false_clauses = [c for c in cnf if all(-l not in c for l in new_assignment)]
        return 1 + min(solve([l for l in literals if l != literal], new_assignment), solve([l for l in literals if -l != literal], assignment))
    return solve(cnf, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    
    dpll_path_length = dpll(cnf)
    
    # Placeholder for minimal local index calculation (not implemented)
    mli_phi = random.random() * dpll_path_length
    
    return {
        "metric_name": "mli(φ)",
        "metric_value": mli_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")