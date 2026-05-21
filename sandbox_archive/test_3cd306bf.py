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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i - 1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def dpll(clauses):
    def search(assignment):
        unsatisfied_clauses = [c for c in clauses if not any(l in assignment and assignment[l] == v for l, v in c)]
        if not unsatisfied_clauses:
            return True, assignment
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            value = True if literal > 0 else False
            new_assignment = {literal: value}
            new_assignment.update(assignment)
            return search(new_assignment)
        pure_literal = next((l for l in range(-40, 41) if (l not in assignment and -l not in assignment)), None)
        if pure_literal is not None:
            value = True if pure_literal > 0 else False
            new_assignment = {pure_literal: value}
            new_assignment.update(assignment)
            return search(new_assignment)
        literal, _ = random.choice(unsatisfied_clauses)
        value = True if literal > 0 else False
        new_assignment = {literal: value}
        new_assignment.update(assignment)
        result, assignment = search(new_assignment)
        if not result:
            new_assignment[literal] = not value
            return search(new_assignment)
        return result, assignment
    
    initial_assignment = {}
    return search(initial_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice(range(-n, n + 1)) for _ in range(random.randint(1, n))]
        if all(l == 0 for l in clause):
            continue
        clauses.append(clause)
    
    result, assignment = dpll(clauses)
    if not result:
        return {
            "metric_name": "depth",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree did not find a solution."
        }
    
    depth = len(assignment)
    return {
        "metric_name": "depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    depth_values = [r["metric_value"] for r in results]
    support_count = sum(r["conjecture_holds"] for r in results)
    support_fraction = Fraction(support_count, len(results))
    
    if support_fraction >= Fraction(90, 100):
        print(f"RESULT: SUPPORTED mean={sum(depth_values) / len(depth_values):.2f} std={math.sqrt(sum((x - sum(depth_values) / len(depth_values)) ** 2 for x in depth_values) / len(depth_values)):.2f} support_fraction={support_fraction}")
    elif any(r["metric_value"] == -1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] == -1)
        print(f"RESULT: FALSIFIED counterexample=\"DPLL search tree did not find a solution.\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")