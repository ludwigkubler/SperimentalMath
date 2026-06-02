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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def matrix_multiplication(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        result = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(A)
        augmented_matrix = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n + 1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if i != j:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[-1] for row in augmented_matrix]
    
    def determinant(A):
        n = len(A)
        if n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def min_order_brauer_group(A):
        n = len(A)
        if n == 1:
            return 1
        for i in range(2, n + 1):
            if all(determinant(matrix_multiplication(A, A)) % p != 0 for p in range(2, i)):
                return i
    
    def communication_complexity_rank(phi):
        # Placeholder function; actual implementation needed based on problem specifics
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_cnf(n)
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    min_order = min_order_brauer_group(A)
    r_phi = communication_complexity_rank(phi)
    
    if min_order == 0:
        return {
            "metric_name": "log2(BrauerGroup)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "min_order_brauer_group returned 0"
        }
    
    log2_brauer_group = math.log2(min_order)
    correlation_coefficient = (log2_brauer_group * r_phi - sum(log2_brauer_group * r for r in range(1, 31)) / 30) / math.sqrt(sum((log2_brauer_group - log2_brauer_group)**2 for _ in range(30)) / 30 * sum((r_phi - r_phi)**2 for _ in range(30)) / 30)
    
    return {
        "metric_name": "log2(BrauerGroup)",
        "metric_value": log2_brauer_group,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient > 0.5 and correlation_coefficient < 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 35)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")