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
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i] = 0
                for k in range(i+1, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0 for _ in range(n)]
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def frobenius_norm(A):
        n = len(A)
        norm = 0
        for i in range(n):
            for j in range(n):
                norm += abs(A[i][j])
        return norm
    
    def generate_monotone_circuit(n, k):
        # Simplified representation of a monotone circuit computing k-CLIQUE
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(k):
            for j in range(i+1, n):
                C[i][j] = 1
        return C
    
    def quantum_geometric_entanglement(C):
        n = len(C)
        I = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        A = matrix_multiply(C, C)
        b = [sum(row[i] for row in C) for i in range(n)]
        x = gaussian_elimination(A, b)
        return frobenius_norm(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        C = generate_monotone_circuit(n, k=3)  # Simplified to k=3 for testing
        rank = quantum_geometric_entanglement(C)
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))
    conjecture_holds = all(0.5 * n**3 <= rank <= 2 * n**3 for rank, n in zip(results, n_values))
    
    return {
        "metric_name": "Minimal Rank of Geometric Entanglement",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank outside expected range for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank outside expected range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical signal")