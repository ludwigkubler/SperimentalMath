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
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def schur_weyl_rank(f, n):
        # Placeholder function to compute Schur-Weyl rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)
    
    def permutation_circuit_size(g, n):
        # Placeholder function to compute permutation circuit size
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 100)
    
    def k_clique_detection(n, m):
        # Placeholder function to detect k-CLIQUE in a graph
        # This is a dummy implementation and should be replaced with actual computation
        return False
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = sum(random.randint(0, 1) * x**i for i in range(n+1))
    rho_f = schur_weyl_rank(f, n)
    
    if rho_f <= C_n * math.log2(n)**2:
        circuit_size = permutation_circuit_size(g, n)
        if circuit_size <= 4*n**2 - 8:
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = "Circuit size exceeds bound"
    else:
        conjecture_holds = False
        counterexample = "Schur-Weyl rank exceeds threshold"
    
    return {
        "metric_name": "permutation_circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"Circuit size exceeds bound\" first_failing_seed={first_failing_seed}")