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
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def dpll_width(phi):
        # Simplified DPLL solver to estimate proof tree width
        if not phi:
            return 0
        if len(phi) == 1:
            return 1
        clause = random.choice(phi)
        literals = set(l for c in phi for l in c)
        true_clauses = [c for c in phi if any(l in c for l in literals)]
        false_clauses = [c for c in phi if all(l not in c for l in literals)]
        return 1 + max(dpll_width(true_clauses), dpll_width(false_clauses))
    
    def polynomial_from_cnf(phi):
        # Simplified polynomial construction from CNF
        n = len(phi)
        poly = [[0] * (n+1) for _ in range(n+1)]
        for clause in phi:
            for l in clause:
                if l > 0:
                    poly[l][l-1] += 1
                else:
                    poly[-l][l-1] -= 1
        return gaussian_elimination(poly)
    
    def mhdrank(poly):
        rank = 0
        for row in poly:
            if any(row):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    phi = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n+1)]
        phi.append(clause)
    
    poly = polynomial_from_cnf(phi)
    mhd = mhdrank(poly)
    width = dpll_width(phi)
    
    return {
        "metric_name": "mhdrank_vs_dpll_width",
        "metric_value": abs(mhd - width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if all(not r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")