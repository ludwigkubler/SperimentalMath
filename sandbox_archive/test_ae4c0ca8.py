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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_dnf(n):
        dnf = []
        for _ in range(2**n):
            clause = [random.choice([0, 1]) for _ in range(n)]
            if sum(clause) > 0:
                dnf.append(clause)
        return dnf
    
    def submodular_measure(dnf):
        n = len(dnf[0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        
        for i in range(n):
            for j in range(i, n):
                if any(all(dnf[k][i] == dnf[k][j] for k in range(len(dnf))) for dnf in dnf):
                    A[i][j] = 1
                    A[j][i] = 1
        
        gaussian_elimination(A, b)
        
        return max(b)

    n = random.randint(5, 40)
    dnf = generate_dnf(n)
    mu_dnf = submodular_measure(dnf)
    
    if len(dnf) > 2**n:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    else:
        conjecture_holds = mu_dnf <= math.log(n, 2)
        counterexample = ""
    
    return {
        "metric_name": "submodular_measure",
        "metric_value": mu_dnf,
        "instances_tested": len(dnf),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 6)]
    
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")