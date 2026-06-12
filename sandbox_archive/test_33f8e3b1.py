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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    if gcd(a, m) != 1:
        raise ValueError("Modular inverse does not exist")
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def matrix_add(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] + B[i][j]) % mod
    return C

def matrix_sub(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] - B[i][j]) % mod
    return C

def matrix_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_transpose(A, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[j][i] = A[i][j]
    return C

def gaussian_elimination(A, b, mod):
    n = len(A)
    Augmented = [row + [val] for row, val in zip(A, b)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i+1, n):
            factor = (Augmented[j][i] * mod_inverse(pivot, mod)) % mod
            for k in range(n + 1):
                Augmented[j][k] = (Augmented[j][k] - factor * Augmented[i][k]) % mod
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (Augmented[i][n] - sum(Augmented[i][j] * x[j] for j in range(i+1, n))) * mod_inverse(Augmented[i][i], mod)
    return x

def xor_matrix(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] ^ B[i][j]
    return C

def dual_linear_code(literals, n):
    code = []
    for literal in literals:
        row = [0] * n
        if literal[0] == 'x':
            index = int(literal[1:]) - 1
            row[index] = 1
        else:
            index = int(literal[2:]) - 1
            row[index] = 1
        code.append(row)
    return code

def clause_entanglement_complexity(code):
    n = len(code)
    F = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if sum(code[i][k] ^ code[j][k] for k in range(n)) == 0:
                F[i][j] = 1
    return F

def minimal_rank(UEA):
    n = len(UEA)
    rank = 0
    for i in range(n):
        if sum(UEA[j][i] for j in range(n)) != 0:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        literals = ['x' + str(i+1) if i % 2 == 0 else 'y' + str(i//2+1) for i in range(n)]
        F = dual_linear_code(literals, n)
        UEA = gaussian_elimination(F, [0] * n, 2)
        
        entanglement_complexity = clause_entanglement_complexity(UEA)
        rank = minimal_rank(UEA)
        
        results.append({
            "n": n,
            "rank": rank,
            "entanglement_complexity": sum(sum(row) for row in entanglement_complexity)
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_entanglement_complexity = sum(result["entanglement_complexity"] for result in results) / len(results)
    correlation_coefficient = 0.0
    
    if len(results) > 1:
        n_mean = sum(result["n"] for result in results) / len(results)
        numerator = sum((result["n"] - n_mean) * (result["rank"] - mean_rank) for result in results)
        denominator = math.sqrt(sum((result["n"] - n_mean) ** 2 for result in results)) * math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_entanglement_complexity <= math.log2(n_mean) + 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")