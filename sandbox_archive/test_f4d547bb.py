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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        pivot = A[i][i]
        for j in range(i + 1, n):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def rank(matrix):
    A = [row[:] + [1] for row in matrix]  # Augmented matrix
    gaussian_elimination(A)
    rank = sum(1 for row in A if any(row[j] != 0 for j in range(len(row) - 1)))
    return rank

def tensor_product(A, B):
    n = len(A)
    return [[[A[i][k] * B[j][l] for l in range(n)] for k in range(n)] for j in range(n)]

def read_twice_bp_width(G):
    # Placeholder function to compute the width of a read-twice branching program
    # This is a dummy implementation and should be replaced with actual logic
    return len(G)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    F = [Fraction(1, 2), Fraction(-1, 2)]  # Example finite field
    
    A = [[random.choice(F) for _ in range(n)] for _ in range(n)]
    B = [[random.choice(F) for _ in range(n)] for _ in range(n)]
    
    np_A_tensor_B = rank(tensor_product(A, B))
    W_G = read_twice_bp_width(G)
    
    metric_value = np_A_tensor_B - (W_G + math.log(n))
    instances_tested = 1
    conjecture_holds = abs(metric_value) <= 3 * math.sqrt(np_A_tensor_B**2 / instances_tested)
    counterexample = "" if conjecture_holds else f"np(A ⊗ B)={np_A_tensor_B}, W(G)={W_G}"
    
    return {
        "metric_name": "Noncommutative Tensor Product Rank vs BP_ReadTwice Width",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='metric_value exceeds 3 std_dev' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")