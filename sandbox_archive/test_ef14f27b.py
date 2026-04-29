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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if i != j:
                factor = A[j][i] / A[i][i]
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    m = n
    ε = 0.1
    
    # Generate a random 3-CNF formula with n variables and m clauses
    clauses = []
    for _ in range(m):
        literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        random.shuffle(literals)
        clause = literals[:3]
        clauses.append(clause)
    
    # Convert the 3-CNF formula to a matrix representation
    A = [[0] * n for _ in range(m)]
    for i, clause in enumerate(clauses):
        for literal in clause:
            var = abs(literal) - 1
            if literal > 0:
                A[i][var] = 1
            else:
                A[i][var] = -1
    
    # Perform Gaussian elimination to find the rank of the matrix
    rank = gaussian_elimination(A)
    rank = sum(1 for row in rank if any(row))
    
    # Calculate the integrality gap
    integrality_gap = 1 - (rank / n)
    
    # Check if the integrality gap is at least 1 - ε
    conjecture_holds = integrality_gap >= 1 - ε
    
    return {
        "metric_name": "integrality_gap",
        "metric_value": integrality_gap,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")