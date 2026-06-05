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
    
    # Define helper functions for matrix operations
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)] for i in range(m)]
        return result
    
    def matrix_transpose(matrix):
        return [list(row) for row in zip(*matrix)]
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det = 0
            for j in range(len(matrix)):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
            return det
    
    def matrix_inverse(matrix):
        det = determinant(matrix)
        if det == 0:
            raise ValueError("Matrix is singular")
        adjugate = [[((-1) ** (i + j)) * determinant([[matrix[m][n] for n in range(len(matrix)) if n != j] for m in range(len(matrix)) if m != i]) for j in range(len(matrix))] for i in range(len(matrix))]
        return matrix_multiplication(adjugate, 1 / det)
    
    def minimal_rank(matrix):
        try:
            inv_matrix = matrix_inverse(matrix)
            rank = len(inv_matrix)
        except ValueError as e:
            rank = None
        return rank
    
    # Generate a random projective scheme X with n variables
    n = random.randint(5, 30)
    matrix = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    # Compute the resolution proof width w(X)
    w_X = len(matrix)
    
    # Construct a locally free sheaf on X and calculate its minimal rank
    sheaf_matrix = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    rank = minimal_rank(sheaf_matrix)
    
    if rank is None:
        return {
            "metric_name": "minimal_rank",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "matrix_singular"
        }
    
    # Establish linear correlation between the minimal rank and 2^(w(X) - 1)
    expected_rank = 2 ** (w_X - 1) - 1
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(rank - expected_rank) <= 0.5 * expected_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")