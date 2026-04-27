# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from collections import defaultdict

def dpll(clauses, assignment):
    if not clauses:
        return True
    var = next(var for var in range(len(assignment)) if assignment[var] is None)
    for val in [True, False]:
        new_assignment = assignment[:]
        new_assignment[var] = val
        new_clauses = [c for c in clauses if not any(l == -var or l == var for l in c)]
        if dpll(new_clauses, new_assignment):
            return True
    return False

def is_unsat(clauses):
    assignment = [None] * len(clauses)
    return not dpll(clauses, assignment)

def count_unsat(clauses):
    n = len(clauses[0])
    count = 0
    for i in range(1 << n):
        assignment = [(i >> j) & 1 for j in range(n)]
        if is_unsat([[l + (n if l < 0 else -n) for l in c] for c in clauses]):
            count += 1
    return count

def indicator_flip(clauses, assignment, var):
    new_assignment = assignment[:]
    new_assignment[var] = not new_assignment[var]
    return is_unsat([[l + (n if l < 0 else -n) for l in c] for c in clauses])

def compute_I(g_F, n):
    I = 0
    for i in range(n):
        count = sum(indicator_flip(clauses, [None] * n, i) for _ in range(1 << (n - 1)))
        I += abs(count / (2 ** (n - 1)) - 0.5)
    return I

def compute_delta(F):
    n = len(F[0])
    m = len(F)
    unsat_count = count_unsat(F)
    if unsat_count == 0:
        return float('inf')
    delta = math.log2(unsat_count) - (n * compute_I(F, n)) / (2 * unsat_count)
    return max(0, delta)

def memoized_minimax(clauses, assignment, depth=0):
    if not clauses:
        return 0
    var = next(var for var in range(len(assignment)) if assignment[var] is None)
    best = float('inf')
    for val in [True, False]:
        new_assignment = assignment[:]
        new_assignment[var] = val
        new_clauses = [c for c in clauses if not any(l == -var or l == var for l in c)]
        best = min(best, memoized_minimax(new_clauses, new_assignment, depth + 1))
    return best

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16]
    results = []
    
    for n in n_values:
        m = max(4 * n // 3, 1)
        unsat_count = 0
        support_count = 0
        
        while unsat_count < 80:
            clauses = []
            for _ in range(m):
                clause = [random.choice([-i-1, i+1] for i in range(n)) for _ in range(3)]
                if is_unsat(clause):
                    clauses.append(clause)
            if len(clauses) == m and not dpll(clauses, [None] * n):
                unsat_count += 1
                g_F = [[l + (n if l < 0 else -n) for l in c] for c in clauses]
                delta = compute_delta(g_F)
                d_T = memoized_minimax(clauses, [None] * n)
                if d_T >= math.ceil(delta):
                    support_count += 1
                results.append((d_T, math.ceil(delta)))
        
        support_fraction = support_count / len(results)
        mean_slack = sum(d_T - math.ceil(delta) for d_T, delta in results) / len(results)
        conjecture_holds = support_fraction >= 0.95 and mean_slack > 0
        
        return {
            "metric_name": "slack",
            "metric_value": mean_slack,
            "instances_tested": len(results),
            "conjecture_holds": conjecture_holds,
            "counterexample": "" if conjecture_holds else f"support_fraction={support_fraction}, mean_slack={mean_slack}"
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    mean_slack = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction={result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")