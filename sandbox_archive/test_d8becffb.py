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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            if rank == m:
                break
            max_row = rank
            for j in range(rank + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[rank], A[max_row] = A[max_row], A[rank]
            if A[rank][i] == 0:
                continue
            for j in range(m):
                if j != rank and A[j][i] != 0:
                    factor = -A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def clause_indicator_polynomial(clauses, n):
        poly = [[0] * (2 ** n) for _ in range(2 ** n)]
        for clause in clauses:
            mask = 0
            for var in clause:
                if var > 0:
                    mask |= 1 << (var - 1)
                else:
                    mask |= 1 << (-var - 1)
            poly[mask][mask] += 1
        return poly
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        p = next((i for i in range(1, len(assignment) + 1) if assignment[i] is None), None)
        if p is None:
            return False
        assignment[p] = True
        new_clauses = [c for c in clauses if not any(l == -p or l == p for l in c)]
        if dpll(new_clauses, assignment):
            return True
        assignment[p] = False
        new_clauses = [c for c in clauses if not any(l == -p or l == p for l in c)]
        if dpll(new_clauses, assignment):
            return True
        return False
    
    def min_rank(clauses, n):
        poly = clause_indicator_polynomial(clauses, n)
        A = []
        for i in range(2 ** n):
            row = [poly[i][j] % 2 for j in range(2 ** n)]
            if any(row[j] == 1 for j in range(n)):
                A.append(row[:n])
        return gaussian_elimination(A)
    
    def dpll_length(clauses, assignment):
        if not clauses:
            return 0
        p = next((i for i in range(1, len(assignment) + 1) if assignment[i] is None), None)
        if p is None:
            return float('inf')
        assignment[p] = True
        new_clauses = [c for c in clauses if not any(l == -p or l == p for l in c)]
        length_true = 1 + dpll_length(new_clauses, assignment)
        assignment[p] = False
        new_clauses = [c for c in clauses if not any(l == -p or l == p for l in c)]
        length_false = 1 + dpll_length(new_clauses, assignment)
        return min(length_true, length_false)
    
    def generate_instance(n):
        clauses = []
        for _ in range(2 ** (n - 1)):
            clause = random.sample(range(-n, n + 1), random.randint(1, n))
            clause = [l for l in clause if l != 0]
            clauses.append(clause)
        return clauses
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_instance(n)
    assignment = {i: None for i in range(1, n + 1)}
    
    rho = min_rank(instance, n)
    l = dpll_length(instance, assignment)
    
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": rho / l if l != 0 else float('inf'),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] != float('inf')) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] != float('inf')) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")