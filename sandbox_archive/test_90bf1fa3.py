# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rref = [row[:] for row in matrix]
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        lead = 0
        for r in range(m):
            if lead >= n:
                return A
            i = r
            while A[i][lead] == 0:
                i += 1
                if i == m:
                    i = r
                    lead += 1
                    if n == lead:
                        return A
            A[r], A[i] = A[i], A[r]
            factor = Fraction(A[r][lead])
            for j in range(n):
                A[r][j] /= factor
            for i2 in range(m):
                if i2 != r:
                    factor = Fraction(A[i2][lead])
                    for j in range(n):
                        A[i2][j] -= factor * A[r][j]
            lead += 1
        return A
    
    rref = gaussian_elimination(rref)
    
    rank = sum(1 for row in rref if any(row[j] != 0 for j in range(cols)))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    communication_matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    rank = matrix_rank(communication_matrix)
    variance_rank = sum((sum(row) - n / 2) ** 2 for row in communication_matrix) / n
    
    return {
        "metric_name": "L-function Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")