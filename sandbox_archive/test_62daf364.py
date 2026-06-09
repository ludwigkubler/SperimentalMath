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
from fractions import Fraction
import math

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def is_satisfiable(phi):
    n = len(phi)
    clauses = phi
    variables = set()
    for clause in clauses:
        variables.update(clause)
    
    assignment = {var: None for var in variables}
    
    def backtrack(assignment, clause_index=0):
        if clause_index == len(clauses):
            return True
        clause = clauses[clause_index]
        for val in [True, False]:
            for var in clause:
                assignment[var] = val
                if all((assignment[var] and (val > 0)) or ((not assignment[var]) and (val < 0)) for var, val in zip(clause, clause)):
                    if backtrack(assignment, clause_index + 1):
                        return True
        return False
    
    return backtrack(assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    variables = list(range(-n, n+1))
    phi = []
    for _ in range(m):
        clause = [random.choice(variables) for _ in range(random.randint(1, n))]
        phi.append(clause)
    
    h_phi = Fraction(m)**Fraction(1, 3)
    satisfiable = is_satisfiable(phi)
    
    return {
        "metric_name": "h_phi",
        "metric_value": float(h_phi),
        "instances_tested": m,
        "n_max": n,
        "conjecture_holds": h_phi <= Fraction(m)**Fraction(1, 3) and satisfiable,
        "counterexample": "" if satisfiable else f"Non-satisfiable with h_phi={h_phi}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_h_phi = sum(res["metric_value"] for res in results) / len(results)
    std_h_phi = math.sqrt(sum((res["metric_value"] - mean_h_phi)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_h_phi} std={std_h_phi} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-satisfiable with h_phi={res['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")