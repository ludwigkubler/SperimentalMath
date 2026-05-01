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
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        factor = 1 / Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] *= factor
        for j in range(n):
            if i != j:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def permanent(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    perm = 0
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        sign = (-1) ** (n - 1 - i)
        perm += sign * A[0][i] * permanent(submatrix)
    return perm

def young_tableaux_decomposition(n):
    def hook_length_formula(tableau):
        n = len(tableau)
        result = 1
        for i in range(n):
            for j in range(n):
                h = n - i + j - 1
                l = min(i, j) + 1
                result *= (h + 1) // math.gcd(h + 1, l)
        return result

    def fill_tableau(tableau, row, col):
        if col == n:
            row += 1
            col = 0
        if row == n:
            return True
        for i in range(1, n + 1):
            if (row > 0 and tableau[row - 1][col] >= i) or (col > 0 and tableau[row][col - 1] >= i):
                continue
            tableau[row][col] = i
            if fill_tableau(tableau, row, col + 1):
                return True
        tableau[row][col] = 0
        return False

    def all_young_tableaux(n):
        tableaus = []
        for _ in range(math.factorial(n)):
            tableau = [[0] * n for _ in range(n)]
            if fill_tableau(tableau, 0, 0):
                tableaus.append(tableau)
        return tableaus

    tableaus = all_young_tableaux(n)
    return [hook_length_formula(t) for t in tableaus]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(1, 3)
    m = math.floor(math.sqrt(n))
    
    perm_tensor = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    det_tensor = [[random.choice([0, 1]) for _ in range(m)] for _ in range(m)]
    
    perm_coeff_sum = sum(young_tableaux_decomposition(n))
    det_coeff_sum = sum(young_tableaux_decomposition(m))
    
    ratio_perm = perm_coeff_sum / (n ** k)
    ratio_det = det_coeff_sum / (m ** k)
    
    conjecture_holds = (ratio_perm > n**(k-1)) and (ratio_det > n**k)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Coefficient Sums",
        "metric_value": ratio_perm,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")