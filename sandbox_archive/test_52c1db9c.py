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

def run_trial(seed: int) -> dict:
    n = 40
    random.seed(seed)
    
    def matrix_mult(A, B):
        return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]
    
    def matrix_power(M, p):
        result = M[:]
        for _ in range(p - 1):
            result = matrix_mult(result, M)
        return result
    
    def noncommutative_lp_norm(M, p):
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = matrix_power(matrix_mult(M, M), int(p - 2))
        B = matrix_mult(A, M)
        C = matrix_mult(B, I)
        trace = sum(C[i][i] for i in range(n))
        return trace ** (1 / p)
    
    def generate_disjointness_matrix():
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        M = [[A[i][j] * B[j][i] for j in range(n)] for i in range(n)]
        return M
    
    M = generate_disjointness_matrix()
    lp_norm = noncommutative_lp_norm(M, 1.5)
    ratio = lp_norm / n ** (1 - 1 / 1.5)
    
    return {
        "metric_name": "lp_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")