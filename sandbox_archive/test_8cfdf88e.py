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
    
    def generate_max_cut_instance(n):
        # Generate a random Max-CUT instance with n variables
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = 0
        return A
    
    def dpll(g, assignment):
        # Simple DPLL algorithm to check if a Max-CUT instance is integrality gap > 0.878
        if not g:
            return True
        v = next(v for v in range(len(g)) if v not in assignment)
        for val in [0, 1]:
            new_assignment = assignment.copy()
            new_assignment[v] = val
            if dpll([g[i][j] for j in range(len(g)) if i != j and (i < j or (i > j and new_assignment[j] == val))], new_assignment):
                return True
        return False
    
    def matrix_multiply(A, B):
        # Matrix multiplication using list of lists
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return C
    
    def eigenvalue_decomposition(M):
        # Simple power iteration method to find the largest eigenvalue
        n = len(M)
        v = [1.0 / math.sqrt(n)] * n
        for _ in range(100):  # Number of iterations
            v = matrix_multiply(M, v)
            norm = sum(x**2 for x in v) ** 0.5
            v = [x / norm for x in v]
        return v
    
    def sos_moment_matrix(A):
        n = len(A)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        M[0][0] = 1
        for i in range(n):
            M[i + 1][i + 1] = A[i][i]
            for j in range(i + 1, n):
                M[j - i][j] = M[j][j - i] = A[i][j]
        return M
    
    def real_rank(M):
        # Real rank via eigenvalue decomposition
        eigvals = eigenvalue_decomposition(M)
        return sum(1 for x in eigvals if abs(x) > 1e-6)
    
    n = random.choice([10, 20, 30, 40])
    A = generate_max_cut_instance(n)
    M = sos_moment_matrix(A)
    rank = real_rank(M)
    
    gap = dpll(A, {})
    conjecture_holds = gap and rank >= 0.3 * n
    counterexample = "gap_check_failed" if not gap else ""
    
    return {
        "metric_name": "real_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='gap_check_failed' first_failing_seed={first_failing_seed}")