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
    
    def generate_symmetric_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_multiplication(A, B):
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
        n = len(A[0])
        augmented_matrix = [A[i] + [b[i]] for i in range(m)]
        for j in range(n):
            max_row = j
            for i in range(j+1, m):
                if abs(augmented_matrix[i][j]) > abs(augmented_matrix[max_row][j]):
                    max_row = i
            augmented_matrix[j], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[j]
            pivot = augmented_matrix[j][j]
            for k in range(n+1):
                augmented_matrix[j][k] /= pivot
            for i in range(m):
                if i != j:
                    factor = augmented_matrix[i][j]
                    for k in range(n+1):
                        augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
        return [row[-1] for row in augmented_matrix[:n]]
    
    def find_smallest_circuit(f):
        # Placeholder for SAT solver implementation
        return len(f)  # Simplified for testing purposes
    
    def symplectic_vectors(matrix):
        m = len(matrix)
        n = len(matrix[0])
        vectors = []
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 1:
                    vector = [0] * n
                    vector[j] = 1
                    vectors.append(vector)
        return vectors
    
    def run_test(n):
        f = generate_symmetric_boolean_function(n)
        M_f = [[f[i + j * (2**(n-1))] for i in range(2**(n-1))] for j in range(2**(n-1))]
        S_f = symplectic_vectors(M_f)
        C_f = find_smallest_circuit(f)
        return len(S_f), len(C_f)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        if n * (n - 1) // 2 > 1000:  # Avoid too large matrices
            continue
        for _ in range(5):
            s, c = run_test(n)
            results.append((s, c))
    
    total_s = sum(s for s, c in results)
    total_c = sum(c for s, c in results)
    mean_s = total_s / len(results)
    mean_c = total_c / len(results)
    support_fraction = len([s for s, c in results if abs(s - 0.5 * c) < 1]) / len(results)
    
    return {
        "metric_name": "symplectic_vectors_to_circuit_ratio",
        "metric_value": mean_s / mean_c,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 30))
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")