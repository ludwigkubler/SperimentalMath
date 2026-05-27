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
    random.seed(seed)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        result = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(b)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
            M[i], M[max_row] = M[max_row], M[i]
            if M[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n + 1):
                    M[j][k] -= factor * M[i][k]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
        return x
    
    def minimal_rank(A):
        rank = 0
        A_copy = [row[:] for row in A]
        for i in range(len(A)):
            if A_copy[i][i] != 0:
                rank += 1
                for j in range(i + 1, len(A)):
                    factor = A_copy[j][i] / A_copy[i][i]
                    for k in range(len(A[0])):
                        A_copy[j][k] -= factor * A_copy[i][k]
        return rank
    
    def symmetry_breaking_communication_complexity(n, t):
        # Placeholder function. Replace with actual implementation.
        return random.randint(1, 2**t)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    t = int(math.log(t))
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    b = [random.randint(-10, 10) for _ in range(n)]
    
    rank = minimal_rank(A)
    comm_complexity = symmetry_breaking_communication_complexity(n, t)
    
    f_t = math.log(t)
    upper_bound = 2**(f_t)
    
    conjecture_holds = rank <= f_t and comm_complexity <= upper_bound
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Symmetry Breaking Communication Complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")