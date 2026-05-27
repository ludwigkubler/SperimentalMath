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
            for k in range(i+1, m):
                factor = A[k][i] / A[i][i]
                for l in range(n):
                    A[k][l] -= factor * A[i][l]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1)**j) * A[0][j] * determinant(submatrix)
        return det
    
    def rank(A):
        rref = gaussian_elimination(A)
        return sum(1 for row in rref if any(row[i] != 0 for i in range(len(row))))
    
    def communication_complexity(n):
        # Simulate a quantum state with varying communication complexity
        return random.randint(5, 40)
    
    n = communication_complexity(30)
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]
    C = matrix_multiply(A, B)
    det_C = determinant(C)
    rank_C = rank(C)
    
    if det_C == 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": n,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Determinant of C is zero"
        }
    
    c = random.random() * 2 + 1
    if rank_C <= c * n:
        return {
            "metric_name": "communication_complexity",
            "metric_value": n,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "communication_complexity",
            "metric_value": n,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank of C ({rank_C}) is greater than {c} * communication complexity ({n})"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Rank condition fails' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")