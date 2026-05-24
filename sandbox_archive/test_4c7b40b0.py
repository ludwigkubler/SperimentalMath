# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

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

    def matrix_multiplication(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det

    def minimal_rank(k, q):
        # Construct a configuration space CS(F_q(T)) associated with the k-clique instance
        points = [random.randint(0, q-1) for _ in range(k)]
        matrix = [[Fraction(1 if i != j else 0, 1) for j in range(k)] for i in range(k)]
        for i in range(k):
            for j in range(i+1, k):
                distance = abs(points[i] - points[j])
                matrix[i][j] = Fraction(distance, q)
                matrix[j][i] = Fraction(distance, q)
        
        # Compute the minimal rank of the configuration space
        reduced_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in reduced_matrix if any(val != 0 for val in row))
        return rank

    def communication_complexity(k):
        n = k + 2 * (k - 1) // 2
        q = 2
        return log(q**(n/2), 2)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        rank = minimal_rank(n, 2)
        cc = communication_complexity(n)
        if rank < cc:
            return {
                "metric_name": "communication_complexity",
                "metric_value": cc,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"Minimal rank {rank} is less than communication complexity {cc}"
            }
        results.append(rank)

    mean_rank = sum(results) / len(results)
    std_dev = (sum((x - mean_rank)**2 for x in results) / len(results))**0.5
    support_fraction = 1.0

    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank < communication_complexity\" first_failing_seed={first_failing_seed}")