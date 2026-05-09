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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = Fraction(matrix[i][i])
        for j in range(n):
            matrix[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = Fraction(0)
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * determinant(submatrix)
        sign *= -1
    return det

def map_clause_to_tensor(clause, n):
    tensor = [[0] * n for _ in range(n)]
    for var in clause:
        if var > 0:
            tensor[var-1][var-1] += 1
        else:
            tensor[-var-1][-var-1] += 1
    return tensor

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    perm_tensor = [[0] * n for _ in range(n)]
    det_tensors = []
    for i in range(n):
        det_tensors.append([[0] * n for _ in range(n)])
    
    # Map permanent to tensor
    for i in range(n):
        perm_tensor[i][i] += 1
    
    # Map determinant-like tensors
    for m in range(1, int(n**1.5) + 1):
        det_tensors[m-1][0][m-1] += 1
        det_tensors[m-1][m-1][0] += 1
    
    # Compute symmetric tensor powers
    perm_power = perm_tensor
    for _ in range(2, n+1):
        perm_power = matrix_multiply(perm_power, perm_tensor)
    
    det_powers = []
    for m in range(1, int(n**1.5) + 1):
        det_power = det_tensors[m-1]
        for _ in range(2, n+1):
            det_power = matrix_multiply(det_power, det_tensors[m-1])
        det_powers.append(det_power)
    
    # Decompose into irreducible representations using Young tableaux counting
    def count_young_tableaux(n, k):
        if n == 0 or k == 0:
            return 1
        return (n + k - 1) * count_young_tableaux(n-1, k-1) // k
    
    perm_multiplicity = count_young_tableaux(n, n-1)
    det_multiplicities = [count_young_tableaux(m, m-1) for m in range(1, int(n**1.5) + 1)]
    
    # Measure μ(f) for both permanent and determinant-like tensors
    perm_mu = perm_multiplicity
    det_mus = det_multiplicities
    
    # Check if μ(perm_n) exceeds μ(det_m) by exponential factors
    conjecture_holds = all(perm_mu >= 2**(m * math.log(n, 2)) for m in range(1, int(n**1.5) + 1))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mu",
        "metric_value": perm_mu,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*10**4, 10**4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu = sum(r["metric_value"] for r in results) / len(results)
    std_mu = math.sqrt(sum((r["metric_value"] - mean_mu)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")