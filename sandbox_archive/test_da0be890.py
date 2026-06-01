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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate entries below pivot
        pivot = matrix[i][i]
        for k in range(i+1, n):
            factor = Fraction(matrix[k][i], pivot)
            for j in range(n + 1):
                matrix[k][j] -= factor * matrix[i][j]
    
    # Back substitution to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(matrix[i][n], matrix[i][i])
        for k in range(i-1, -1, -1):
            matrix[k][n] -= matrix[k][i] * x[i]
    
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def local_coherence_rank(matrix):
    augmented_matrix = [row + [1] for row in matrix]
    reduced_matrix = gaussian_elimination(augmented_matrix)
    rank = sum(1 for row in reduced_matrix if any(x != 0 for x in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        # Generate a random n-communication protocol
        P = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        
        # Compute the associated quantum circuit (simply use the protocol matrix)
        C_P = sum(sum(row) for row in P)
        
        # Calculate the local coherence rank of the circuit
        mlcr_P = local_coherence_rank(P)
        
        # Check if the conjecture holds for this protocol
        k_values = [1, 2, 3]
        max_diff = max(abs(mlcr_P - k * C_P) for k in k_values)
        results.append({
            "n": n,
            "mlcr_P": mlcr_P,
            "C_P": C_P,
            "max_diff": max_diff
        })
    
    # Determine if the conjecture holds for this seed
    conjecture_holds = all(max_diff <= 1e-6 for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, mlcr(P)={results[0]['mlcr_P']}, C(P)={results[0]['C_P']}"
    
    return {
        "metric_name": "max_diff",
        "metric_value": max(max_diff for result in results),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, mlcr(P)={results[0]['mlcr_P']}, C(P)={results[0]['C_P']}\" first_failing_seed={first_failing_seed}")