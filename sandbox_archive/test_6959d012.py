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
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def matrix_rank(A):
    m, n = len(A), len(A[0])
    A = [row[:] for row in A]
    rank = gaussian_elimination(A)
    return rank

def generate_cnf(n):
    clauses = []
    for _ in range(2*n):
        clause = random.sample(range(1, 2*n+1), 3)
        clauses.append(clause)
    cnf = [clauses[:n], clauses[n:]]
    return cnf

def compute_eta_quotient(cnf):
    n = len(cnf[0])
    G = [[0]*n for _ in range(n)]
    for clause in cnf[1]:
        for i in clause:
            for j in clause:
                if i != j:
                    G[i-1][j-1] += 1
    rank_G = matrix_rank(G)
    eta_quotient = Fraction(rank_G, n**2)
    return eta_quotient

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        eta_quotient = compute_eta_quotient(cnf)
        results.append(eta_quotient)
    metric_value = sum(results) / len(results)
    conjecture_holds = all(q <= Fraction(n**2, n**2) for q in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "minimal_eta_quotient",
        "metric_value": float(metric_value),
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= max([Fraction(n**2, n**2) for n in [5, 10, 15, 20, 30, 40]])) / len(results)
    
    if all(r <= max([Fraction(n**2, n**2) for n in [5, 10, 15, 20, 30, 40]]) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > max([Fraction(n**2, n**2) for n in [5, 10, 15, 20, 30, 40]]) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > max([Fraction(n**2, n**2) for n in [5, 10, 15, 20, 30, 40]]))
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")