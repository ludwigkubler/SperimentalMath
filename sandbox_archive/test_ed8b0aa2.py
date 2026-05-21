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
        if len(A[0]) != len(B):
            return None
        result = [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]
        return result
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [0] for row in matrix]
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                return None
            for j in range(n):
                augmented_matrix[i][j] /= pivot
            for k in range(n + 1):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(n):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[:-1] for row in augmented_matrix]
    
    def determinant(matrix):
        n = len(matrix)
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def is_invertible(matrix):
        return determinant(gaussian_elimination(matrix)) != 0
    
    def generate_disjointness_matrix(n):
        X = list(range(n))
        Y = list(range(n, 2*n))
        M = [[1 if i in X and j in Y else 0 for j in range(2*n)] for i in range(n)]
        return M
    
    def communication_complexity(M):
        n = len(M)
        total_bits = 0
        for row in M:
            bits = sum(1 for x in row if x == 1)
            total_bits += math.ceil(math.log2(bits + 1))
        return total_bits
    
    def geometric_invariant(M):
        rank = 0
        submatrix = [row[:] for row in M]
        while is_invertible(submatrix):
            rank += 1
            submatrix.pop(0)
        return rank
    
    n = random.randint(5, 40)
    M_f = generate_disjointness_matrix(n)
    gamma_M_f = geometric_invariant(M_f)
    comm_f = communication_complexity(M_f)
    
    if gamma_M_f == 0:
        return {
            "metric_name": "gamma(M_f)",
            "metric_value": gamma_M_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c = 1 / math.log2(n)
    if comm_f < c * gamma_M_f:
        return {
            "metric_name": "gamma(M_f)",
            "metric_value": gamma_M_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"comm(f) = {comm_f}, c*gamma(M_f) = {c * gamma_M_f}"
        }
    
    return {
        "metric_name": "gamma(M_f)",
        "metric_value": gamma_M_f,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
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
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")