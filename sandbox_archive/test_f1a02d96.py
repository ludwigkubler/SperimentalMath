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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def noncommutative_Lp_norm(M, p):
        n = len(M)
        sum_val = 0
        for i in range(n):
            for j in range(i + 1, n):
                norm_ij = abs(sum(M[i][k] * M[j][k] for k in range(n)))
                if norm_ij != 0:
                    sum_val += norm_ij ** (p / (i + j - 2))
        return sum_val
    
    def generate_entanglement_matrix(n):
        # Simplified entanglement matrix generation
        M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        return gaussian_elimination(M)
    
    n = random.randint(5, 40)
    M = generate_entanglement_matrix(n)
    p_values = [1] + list(range(2, 10)) + [math.inf]
    c = 1.0 / n
    
    results = []
    for p in p_values:
        norm = noncommutative_Lp_norm(M, p)
        if norm < c * n:
            return {
                "metric_name": "Noncommutative L_p Norm",
                "metric_value": norm,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Norm {norm} is less than cn = {c * n}"
            }
        results.append(norm)
    
    return {
        "metric_name": "Noncommutative L_p Norm",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(p_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= c * n) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < c * n for r in results):
        first_failing_seed = next(i + 1 for i, r in enumerate(results) if r < c * n)
        print(f"RESULT: FALSIFIED counterexample='Norm less than cn' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")