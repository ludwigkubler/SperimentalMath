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

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def random_permutation(n):
    perm = list(range(n))
    random.shuffle(perm)
    return perm

def dpll(instance, order):
    def solve(index):
        if index == len(instance):
            return True
        var = instance[index][0]
        for val in [True, False]:
            assignment[var] = val
            clause_sat = any(any(assignment[v] == (not c) for v, c in clause) for clause in instance[index])
            if clause_sat and solve(index + 1):
                return True
            assignment.pop(var)
        return False

    n = len(instance)
    assignment = {}
    order_set = set(order)
    stack = []
    while stack or order:
        while stack and (stack[-1] not in order_set or assignment[stack[-1]] is not None):
            stack.pop()
        if not stack:
            var = next(v for v in order if v not in assignment)
            stack.append(var)
            assignment[var] = True
        else:
            var = stack[-1]
            assignment[var] = False
            stack.pop()
    return solve(0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [12, 16, 20, 24]
    results = []
    
    for n in n_values:
        phi = (math.sqrt(5) - 1) / 2
        instance = [[random.randint(1, n), random.choice([True, False]), random.choice([True, False])] for _ in range(8 * n)]
        order_phi = sorted(range(n), key=lambda i: (i * phi) % 1)
        
        T_phi = dpll(instance, order_phi)
        T_R_values = [dpll(instance, random_permutation(n)) for _ in range(30)]
        mean_T_R = sum(T_R_values) / len(T_R_values)
        
        results.append({
            "n": n,
            "T_phi": T_phi,
            "mean_T_R": mean_T_R
        })
    
    max_diff = max(result["T_phi"] - result["mean_T_R"] for result in results)
    rho = sum((result["T_phi"] - mean_T_R) * (math.log2(result["T_phi"]) - math.log2(mean_T_R)) for result in results) / (len(results) * (sum((result["T_phi"] - mean_T_R) ** 2 for result in results) / len(results) - (sum((math.log2(result["T_phi"]) - math.log2(mean_T_R)) ** 2 for result in results) / len(results))) ** 0.5)
    
    conjecture_holds = max_diff <= 4 * math.log2(24) and rho >= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "max_diff",
        "metric_value": max_diff,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_max_diff = sum(result["metric_value"] for result in results) / len(results)
    std_max_diff = (sum((result["metric_value"] - mean_max_diff) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_max_diff} std={std_max_diff} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")