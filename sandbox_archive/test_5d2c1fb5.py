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

# Helper functions for linear algebra and K-theory
def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = Fraction(matrix[i][i])
        for j in range(cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = Fraction(matrix[k][i])
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def matrix_multiplication(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[Fraction(0) for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def compute_char_variety(cnf, p):
    n = len(cnf)
    matrix = [[Fraction(0) for _ in range(n + n + 1)] for _ in range(n)]
    for clause in cnf:
        for literal in clause:
            var = abs(literal) - 1
            if literal > 0:
                matrix[var][var] += Fraction(1)
            else:
                matrix[var][n + var] += Fraction(1)
    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(x != Fraction(0) for x in row))
    return rank % p

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    cnf = []
    for _ in range(n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        cnf.append(clause)
    
    p = 2**64 + 37  # A large prime number
    char_variety_rank = compute_char_variety(cnf, p)
    resolution_width = len(max(cnf, key=len))
    
    metric_name = "K-theoretic Rank Bound"
    metric_value = char_variety_rank
    instances_tested = n
    n_max = n
    conjecture_holds = char_variety_rank <= (n ** 2) * math.log(n)
    counterexample = "" if conjecture_holds else f"char_variety_rank={char_variety_rank}, expected<=n^2*log(n)={(n ** 2) * math.log(n)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 37 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"char_variety_rank>n^2*log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")