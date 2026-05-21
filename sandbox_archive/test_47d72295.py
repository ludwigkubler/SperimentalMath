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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def nuclear_norm(M):
        U, _, Vt = gaussian_elimination(matrix_multiply(M, M))
        singular_values = [math.sqrt(U[i][i]*Vt[i][i]) for i in range(min(len(U), len(Vt)))]
        return sum(singular_values)
    
    n = random.choice([8, 10, 12, 14, 16])
    w = random.choice([2, 3, 4])
    s = 2**w
    IP_2_trivial = [[(-1)**(i^j) for j in range(n//2)] for i in range(n//2)]
    
    def f(x, y):
        return (-1)**((x & (1 << n//2 - 1)) ^ (y & (1 << n//2 - 1)))
    
    M = [[f(i, j) for j in range(2**(n//2))] for i in range(2**(n//2))]
    rho_P = math.log2(nuclear_norm(M) / 2**(n//2))
    
    return {
        "metric_name": "rho(P)",
        "metric_value": rho_P,
        "instances_tested": 1,
        "conjecture_holds": rho_P <= 4 * math.log2(s + 1) + 1,
        "counterexample": "" if rho_P <= 4 * math.log2(s + 1) + 1 else f"rho(P) = {rho_P} > 4 * log2({s+1}) + 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho_P = sum(r["metric_value"] for r in results) / len(results)
    std_rho_P = math.sqrt(sum((r["metric_value"] - mean_rho_P)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_P} std={std_rho_P} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")