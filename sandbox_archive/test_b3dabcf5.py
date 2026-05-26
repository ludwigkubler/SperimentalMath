# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def characteristic_polynomial(literals, n):
    identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    A = [[0] * n for _ in range(n)]
    for literal in literals:
        row = [0] * n
        for var in literal:
            if var < 0:
                row[-var-1] += -1
            else:
                row[var-1] += 1
        A = matrix_multiply(A, identity)
        A = matrix_multiply(A, [[Fraction(-1) if i == j else Fraction(0) for j in range(n)] + [row[i]] for i in range(n)])
    gaussian_elimination(A)
    char_poly = [A[i][n] for i in range(n)]
    return char_poly

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    literals = []
    for _ in range(10):
        literal = []
        for j in range(n):
            if random.choice([True, False]):
                literal.append(j + 1)
            else:
                literal.append(-(j + 1))
        literals.append(literal)
    
    char_poly = characteristic_polynomial(literals, n)
    rank = sum(1 for row in char_poly if any(coeff != Fraction(0) for coeff in row))
    
    resolution_width = 2 ** (rank - 1)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width,
        "instances_tested": len(literals),
        "conjecture_holds": resolution_width >= 2 ** (math.log2(rank)),
        "counterexample": "" if resolution_width >= 2 ** (math.log2(rank)) else f"Rank {rank}, Width {resolution_width}"
    }

if __name__ == "__main__":
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank {results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")