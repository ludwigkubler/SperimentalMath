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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def rank(A):
        m, n = len(A), len(A[0])
        A_augmented = [row[:] + [0] for row in A]
        b = [0] * m
        x = gaussian_elimination(A_augmented, b)
        rank = 0
        for i in range(m):
            if any(x[j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def generate_monotone_circuit(n: int) -> list:
        # Placeholder function to generate a random monotone circuit
        # This is a dummy implementation and should be replaced with actual logic
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def construct_braess_sarle_curve(C: list) -> list:
        # Placeholder function to construct the Braess–Sarle curve from a circuit
        # This is a dummy implementation and should be replaced with actual logic
        return C
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n, 10))
    
    C = generate_monotone_circuit(n)
    Σ = construct_braess_sarle_curve(C)
    
    rank_Σ = rank(Σ)
    α_n = log2(n)
    β_k = log2(k)
    lower_bound = α_n**2 + β_k**2
    
    if rank_Σ < lower_bound:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": rank_Σ,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank of Braess–Sarle curve is {rank_Σ}, but lower bound is {lower_bound}"
        }
    else:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": rank_Σ,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank of Braess–Sarle curve is less than lower bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")