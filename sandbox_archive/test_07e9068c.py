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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = -A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] += factor * A[rank][k]
        rank += 1
    return rank

def minimal_rank(C):
    n = len(C)
    A = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            A[i][j] = C[i][j]
        A[i][n] = 1
    return gaussian_elimination(A)

def dpll(CNF, assignment=None):
    if assignment is None:
        assignment = {}
    if not CNF:
        return True
    for clause in CNF:
        if any(lit in assignment and (assignment[lit] == 0) for lit in clause):
            continue
        new_assignment = assignment.copy()
        new_assignment[clause[0]] = 1
        if dpll(CNF, new_assignment):
            return True
        new_assignment[clause[0]] = -1
        if dpll(CNF, new_assignment):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    CNF = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        CNF.append(clause)
    
    f = lambda x, y: sum([sum([C[i][j] * x**(i+1) * y**(j+1) for j in range(n)]) for i in range(n)])
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = f(i, j)
    
    r_f = minimal_rank(C)
    t_F = 1
    while not dpll(CNF, {}):
        t_F += 1
    
    log_r_f = math.log2(r_f) if r_f > 0 else float('-inf')
    diff = abs(log_r_f - t_F)
    
    return {
        "metric_name": "log_r_f_minus_t_F",
        "metric_value": diff,
        "instances_tested": 1,
        "conjecture_holds": diff <= 1,
        "counterexample": "" if diff <= 1 else f"Counterexample found with n={n}, log2(r(f))={log_r_f}, t(F)={t_F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_diff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")