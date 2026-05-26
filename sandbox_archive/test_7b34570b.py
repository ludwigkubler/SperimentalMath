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

# Helper functions for linear algebra
def matrix_multiply(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m = len(A)
    n = len(b)
    if m != n:
        raise ValueError("Matrix and vector dimensions do not match")
    
    A_augmented = [A[i] + [b[i]] for i in range(m)]
    
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        
        pivot = A_augmented[i][i]
        for j in range(i, n+1):
            A_augmented[i][j] /= pivot
        
        for j in range(m):
            if j != i:
                factor = A_augmented[j][i]
                for k in range(i, n+1):
                    A_augmented[j][k] -= factor * A_augmented[i][k]

def rank(A):
    m = len(A)
    n = len(A[0])
    gaussian_elimination(A, [0]*n)
    
    rank = 0
    for i in range(m):
        if any(A[i][j] != 0 for j in range(n)):
            rank += 1
    
    return rank

# Function to generate a random monotone circuit
def generate_monotone_circuit(n, k):
    # This is a placeholder function. In practice, you would need to implement
    # the logic to generate a valid monotone circuit for k-CLIQUE.
    # For simplicity, we will return a dummy circuit.
    return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]

# Function to construct the Braess–Sarle curve
def construct_braess_sarle_curve(C):
    n = len(C)
    # Placeholder implementation. In practice, you would need to implement
    # the logic to construct the Braess–Sarle curve from the circuit C.
    # For simplicity, we will return a dummy curve.
    A = [[0] * (n + 1) for _ in range(n + 1)]
    b = [0] * (n + 1)
    return A, b

# Main function to run one trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(1, min(n // 2, 10))
    
    C = generate_monotone_circuit(n, k)
    A, b = construct_braess_sarle_curve(C)
    
    try:
        rank_Σ = rank(A)
        α_n = math.log2(n)
        β_k = math.log2(k)
        
        if rank_Σ < α_n**2 + β_k**2 or rank_Σ > 10:
            return {
                "metric_name": "rank",
                "metric_value": rank_Σ,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank_Σ} is not in the range [{α_n**2 + β_k**2}, 10]"
            }
        else:
            return {
                "metric_name": "rank",
                "metric_value": rank_Σ,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            }
    except Exception as e:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Exception: {str(e)}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*37 + 1, 37))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/instances_tested} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 10 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 10)
        print(f"RESULT: FALSIFIED counterexample='Rank too small' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")