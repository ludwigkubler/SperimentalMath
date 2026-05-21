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

def random_matrix(n):
    return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    sign = 1
    for j in range(len(matrix)):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * determinant(submatrix)
        sign *= -1
    return det

def character_projection(M, λ):
    n = len(M)
    if len(λ) != n:
        return 0
    product = 1
    for i in range(n):
        for j in range(n):
            if (i + 1) * (j + 1) <= n * n and (i + 1) % λ[i] == 0 and (j + 1) % λ[j] == 0:
                product *= M[i][j]
    return abs(product)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = 20
    max_lambda_size = math.floor(n ** 1.5)
    
    M = random_matrix(n)
    det_M = determinant(M)
    perm_n = [i for i in range(1, n + 1)]
    det_perm_n = determinant([[perm_n[j - 1] if j == i else 0 for j in range(1, n + 1)] for i in range(1, n + 1)])
    
    max_projection = 0
    for λ in itertools.combinations_with_replacement(range(1, n + 1), len(λ)):
        if sum(λ) > max_lambda_size:
            break
        proj_M = character_projection(M, λ)
        proj_perm_n = character_projection([[perm_n[j - 1] if j == i else 0 for j in range(1, n + 1)] for i in range(1, n + 1)], λ)
        max_projection = max(max_projection, proj_M, proj_perm_n)
    
    metric_value = max_projection
    instances_tested = len(list(itertools.combinations_with_replacement(range(1, n + 1), len(λ))))
    conjecture_holds = det_M < perm_n and det_M < m
    counterexample = "" if conjecture_holds else f"det(M)={det_M}, det(perm_n)={perm_n}"
    
    return {
        "metric_name": "character_projection",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"det(M) < det(perm_n)\" first_failing_seed={first_failing_seed}")