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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def lex_dpll(F, assignment):
    if not F:
        return True
    var = next(v for v in range(len(assignment)) if assignment[v] is None)
    for val in [0, 2]:
        new_assignment = assignment[:]
        new_assignment[var] = val
        if all(new_assignment[v] == (F[i][v] > 0) * 2 - 1 for i in range(len(F))):
            if lex_dpll(F, new_assignment):
                return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 7, 8, 9, 10, 11]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        alpha = 5.0
        F_count = 40
        d_DPLL_sum = 0
        
        for _ in range(F_count):
            variables = list(range(n))
            clauses = []
            for _ in range(int(alpha * n * (n - 1) / 6)):
                clause = random.sample(variables, 3)
                if random.choice([True, False]):
                    clause = [-v for v in clause]
                clauses.append(clause)
            
            F = [[0] * n for _ in range(n)]
            for clause in clauses:
                for l in clause:
                    i = abs(l) - 1
                    F[i][i] += (-1 if l < 0 else 1)
            
            d_DPLL_F = lex_dpll(F, [None] * n)
            d_DPLL_sum += d_DPLL_F
            
            H_F = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    H_F[i][j] = sum((-1 if l < 0 else 1) * (-1 if m < 0 else 1) for l, m in zip(F[i], F[j]))
            
            rank_F = gaussian_elimination(H_F)
            
            instances_tested += 1
            if rank_F < d_DPLL_F:
                conjecture_holds = False
                counterexample = f"n={n}, alpha=5.0, d_DPLL(F)={d_DPLL_F}, rank_F={rank_F}"
    
    mean_d_DPLL = d_DPLL_sum / instances_tested
    std_d_DPLL = math.sqrt(sum((d_DPLL - mean_d_DPLL) ** 2 for d_DPLL in range(d_DPLL_sum // instances_tested, d_DPLL_sum // instances_tested + 1)) / instances_tested)
    
    return {
        "metric_name": "DPLL Depth",
        "metric_value": mean_d_DPLL,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d_DPLL = sum(r["metric_value"] for r in results) / len(results)
    std_d_DPLL = math.sqrt(sum((r["metric_value"] - mean_d_DPLL) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d_DPLL} std={std_d_DPLL} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.95:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")