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
    A = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        if A[i][i] == 0:
            return None  # No unique solution
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            A[j] = [A[j][k] + factor * A[i][k] for k in range(n+1)]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def dpll(instance, assignment=None):
    if assignment is None:
        assignment = {}
    n = len(instance)
    unit_clauses = [i for i in range(n) if instance[i] and -instance[i].count(0) == 1]
    while unit_clauses:
        var = unit_clauses.pop()
        value = 1 if any(c[var] > 0 for c in instance) else -1
        assignment[var] = value
        new_clauses = []
        for clause in instance:
            if not any(abs(lit) == var for lit in clause):
                new_clause = [lit for lit in clause if lit != -var]
                if new_clause:
                    new_clauses.append(new_clause)
        instance = new_clauses

    unsatisfied_clauses = [c for c in instance if all(lit not in assignment or assignment[lit] == 0 for lit in c)]
    if not unsatisfied_clauses:
        return True
    var = next(v for v in range(n) if v not in assignment)
    pos_clauses = [c for c in instance if var in c or -var in c]
    neg_clauses = [c for c in instance if -var in c and all(lit not in assignment or assignment[lit] == 0 for lit in c)]
    return dpll(pos_clauses, assignment.copy()) or dpll(neg_clauses, assignment.copy())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = [[random.randint(-n, n) for _ in range(n)] for _ in range(n)]
    height = dpll(instance)
    if height is None:
        return {
            "metric_name": "DPLL Height",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "No unique solution"
        }
    return {
        "metric_name": "DPLL Height",
        "metric_value": height,
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='DPLL height is unbounded' first_failing_seed={first_failing_seed}")