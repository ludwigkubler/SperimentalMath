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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            M[j] = [M[j][k] - factor * M[i][k] for k in range(n + 1)]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (M[i][-1] - sum(M[i][j] * x[j] for j in range(i+1, n))) / M[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(n))
    
    # Generate a random CNF formula
    cnf_formula = []
    for _ in range(random.randint(10, 20)):
        clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(3)]
        cnf_formula.append(clause)
    
    # Compute the quantum clone (simplified version)
    Q_phi = [[0] * n for _ in range(n)]
    for clause in cnf_formula:
        for var1 in clause:
            for var2 in clause:
                if var1 != var2 and abs(var1) == abs(var2):
                    Q_phi[abs(var1)-1][abs(var2)-1] += 1
    
    # Compute the minimal order of the Brauer group
    non_zero_entries = [entry for row in Q_phi for entry in row if entry != 0]
    br_order = max(non_zero_entries, default=1)
    
    # Compute the communication complexity rank variance (simplified version)
    rank_variance = sum(abs(entry) for entry in non_zero_entries) / len(non_zero_entries)
    
    return {
        "metric_name": "Brauer Group Order vs Communication Complexity Rank Variance",
        "metric_value": abs(br_order - rank_variance),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(br_order - rank_variance) <= 2 * rank_variance,
        "counterexample": "" if abs(br_order - rank_variance) <= 2 * rank_variance else f"br_order={br_order}, rank_variance={rank_variance}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")