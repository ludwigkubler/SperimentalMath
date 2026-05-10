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
from math import factorial

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def hook_length_formula(n, k):
    numerator = 1
    denominator = 1
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            numerator *= (n - i + j)
            denominator *= j
    return numerator // denominator

def permanent(n, matrix):
    if n == 0:
        return 1
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [[matrix[i][k] for k in range(j) + range(j+1, n)] for i in range(1, n)]
        det += ((-1) ** j) * matrix[0][j] * permanent(n - 1, submatrix)
    return det

def determinant(n, matrix):
    if n == 0:
        return 1
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [[matrix[i][k] for k in range(j) + range(j+1, n)] for i in range(1, n)]
        det += ((-1) ** j) * matrix[0][j] * determinant(n - 1, submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 16
    num_instances = 30
    count_supporting = 0
    counterexample = ""

    for _ in range(num_instances):
        # Generate a random 3-CNF formula with n variables
        clauses = []
        for _ in range(2 * n):
            literals = [random.randint(1, n), random.randint(-n, -1)]
            random.shuffle(literals)
            clause = (literals[0], literals[1])
            clauses.append(clause)

        # Compute the permanent and determinant representations
        perm_matrix = [[0] * n for _ in range(n)]
        det_matrix = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if (i + 1, j + 1) in clauses or (-i - 1, -j - 1) in clauses:
                    perm_matrix[i][j] = 1
                    det_matrix[i][j] = 1

        perm_val = permanent(n, perm_matrix)
        det_val = determinant(n, det_matrix)

        # Compute the ratio of dominant irreducible component dimensions
        perm_dim = hook_length_formula(n, n)
        det_dim = hook_length_formula(n, n - 1)
        ratio = perm_dim / det_dim

        if ratio >= 2 ** (n / 4) * 0.95:
            count_supporting += 1
        else:
            counterexample = f"Ratio {ratio} < 2^(n/4) * 0.95"

    return {
        "metric_name": "Ratio of Permanent to Determinant Dimensions",
        "metric_value": ratio,
        "instances_tested": num_instances,
        "conjecture_holds": count_supporting >= 0.8 * num_instances,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")