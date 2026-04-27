# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                max_row = j
        A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
        factor = A_b[i][i]
        for j in range(n + 1):
            A_b[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = A_b[j][i]
                for k in range(n + 1):
                    A_b[j][k] -= factor * A_b[i][k]
    return [row[-1] for row in A_b]

def unit_propagation(clauses, assignment):
    while True:
        new_assignment = False
        for clause in clauses:
            if all(lit not in assignment or (lit < 0) == (assignment[lit] is False) for lit in clause):
                continue
            unassigned_lits = [lit for lit in clause if lit not in assignment]
            if len(unassigned_lits) == 1:
                new_assignment = True
                assignment[unassigned_lits[0]] = (unassigned_lits[0] > 0)
        if not new_assignment:
            break
    return assignment

def dpll(clauses, assignment):
    n = max(abs(lit) for clause in clauses for lit in clause)
    if all(lit in assignment or (lit < 0) == (assignment[-lit] is False) for clause in clauses):
        return len(assignment)
    unassigned_vars = [var for var in range(-n, 0) if var not in assignment]
    var = unassigned_vars[0]
    assignment[var] = True
    result = dpll(clauses, assignment)
    if result is not None:
        return result
    assignment[var] = False
    return dpll(clauses, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16, 18, 20])
    alpha = 4.0
    m = int(alpha * n * (n - 1) / 6)
    clauses = []
    for _ in range(m):
        while True:
            lits = random.sample(range(-n, 0), 3)
            if len(set(lits)) == 3 and all(abs(lit) != abs(lit2) for lit, lit2 in zip(lits, lits[1:])):
                clauses.append(lits)
                break
    assignment = {}
    C_F = None
    for k in range(1, n + 1):
        for subset in itertools.combinations(range(-n, 0), k):
            sub_clauses = [clause for clause in clauses if any(lit in subset for lit in clause)]
            if unit_propagation(sub_clauses, assignment) is None:
                C_F = k
                break
        if C_F is not None:
            break
    
    D_F = dpll(clauses, {})
    
    if D_F is None or D_F > 3 * C_F + math.ceil(math.log2(n)) + 2:
        return {
            "metric_name": "DPLL Depth",
            "metric_value": D_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"D(F) > 3*C(F) + log2(n) + 2"
        }
    
    return {
        "metric_name": "DPLL Depth",
        "metric_value": D_F,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.90 and all(res["support_fraction"] >= 0.80 for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(res["conjecture_holds"] is False for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"D(F) > 3*C(F) + log2(n) + 2\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.90")