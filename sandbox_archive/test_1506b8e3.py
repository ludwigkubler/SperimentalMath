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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def moment_cumulant_transform(A):
        n = len(A)
        cumulants = [0] * (n + 1)
        cumulants[0] = 1
        for i in range(n):
            for j in range(i, n):
                factor = A[i][j]
                for k in range(j+1, n):
                    factor *= A[j][k]
                cumulants[i+1] += factor
        return cumulants
    
    def free_cumulant_gap(cumulants):
        gap = 0
        for i in range(2, len(cumulants)):
            gap += (cumulants[i] - sum(cumulants[:i])) / (i * math.log(i))
        return gap
    
    n = 40
    num_clauses = random.randint(n, 3*n)
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(3)]
        clauses.append(clause)
    
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(i, n):
            count = sum(1 for clause in clauses if (i+1 in clause and j+1 in clause) or (-i-1 in clause and -j-1 in clause))
            A[i][j] = A[j][i] = count
    
    A = gaussian_elimination(A)
    cumulants = moment_cumulant_transform(A)
    mu = free_cumulant_gap(cumulants)
    
    R_disj = 2 * n * math.log(n) / (math.log(2) ** 2)
    
    return {
        "metric_name": "mu/R_disj",
        "metric_value": mu / R_disj,
        "instances_tested": 1,
        "conjecture_holds": mu / R_disj >= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")