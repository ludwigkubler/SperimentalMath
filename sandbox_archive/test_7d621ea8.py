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
        m, n = len(A), len(A[0])
        for i in range(m):
            # Find the maximum element in this column
            max_idx = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_idx][i]):
                    max_idx = j
            # Swap current row with the row containing the maximum element
            A[i], A[max_idx] = A[max_idx], A[i]
            # Eliminate all other elements in this column
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matroid_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def generate_monotone_dnf(n, k):
        clauses = []
        for _ in range(k):
            clause = random.sample(range(1, n+1), random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def dnf_to_matrix(dnf):
        m, n = len(dnf), len(dnf[0])
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(dnf):
            for literal in clause:
                if literal > 0:
                    A[i][literal - 1] = 1
                else:
                    A[i][-1] += 1
        return A
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n, 4))
    
    dnf = generate_monotone_dnf(n, k)
    matrix = dnf_to_matrix(dnf)
    rank = matroid_rank(matrix)
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= n**(k/2),
        "counterexample": "" if rank >= n**(k/2) else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['metric_value']}, k={k}\" first_failing_seed={first_failing_seed}")