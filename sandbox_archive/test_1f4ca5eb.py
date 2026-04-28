# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_inv(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    I[k][j] -= factor * I[i][j]
    return I

def schur_defect(v, n):
    lambda_v = sorted(v)
    K = [[0] * (n + 1) for _ in range(n + 1)]
    for mu in range(1 << n):
        count = 0
        for i in range(n):
            if mu & (1 << i):
                count += 1
        K[mu][count] += 1

    inv_K = matrix_inv(K)
    defect = sum(max(0, -inv_K[i][j]) for i in range(n + 1) for j in range(n + 1))
    return defect

def lex_dpll(F):
    n = len(F)
    assignment = [None] * n
    stack = []
    def backtrack():
        if all(assignment):
            return True
        var = next(i for i in range(n) if assignment[i] is None)
        assignment[var] = True
        stack.append((var, True))
        if lex_dpll(F):
            return True
        assignment[var] = False
        stack.pop()
        assignment[var] = True
        stack.append((var, False))
        if lex_dpll(F):
            return True
        stack.pop()
        return False
    return backtrack()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6, 7, 8, 9]
    results = []
    for n in n_values:
        F = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n + 1)]
        v = [sum(F[j][i] for j in range(n + 1)) for i in range(n)]
        lambda_v = sorted(v)
        defect = schur_defect(v, n)
        if n <= 7:
            L_TF = lex_dpll(F)
        else:
            # Upper bound via bisection
            low, high = 0, n + 1
            while low < high:
                mid = (low + high) // 2
                F_upper = [[random.choice([0, 1]) for _ in range(n)] for _ in range(mid)]
                if lex_dpll(F_upper):
                    low = mid + 1
                else:
                    high = mid
            L_TF = low - 1
        results.append({
            "n": n,
            "L_TF": L_TF,
            "defect": defect,
            "log2_L_TF": log2(L_TF) if L_TF > 0 else float('-inf'),
            "S_F": defect + 1
        })
    metric_value = sum(result["log2_L_TF"] for result in results)
    instances_tested = len(results)
    conjecture_holds = all(result["log2_L_TF"] >= (result["defect"] + 1) / 4 for result in results)
    counterexample = "" if conjecture_holds else "n={}".format(next(n for n, result in enumerate(results) if result["log2_L_TF"] < (result["defect"] + 1) / 4))
    return {
        "metric_name": "log2(L_TF)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [11, 23, 37, 53, 71]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")