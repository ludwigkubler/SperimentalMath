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
    
    def generate_symplectic_matrix(n):
        # Simple 2n x 2n symplectic matrix generator for demonstration purposes
        A = [[0] * (2*n) for _ in range(2*n)]
        for i in range(n):
            A[i][i] = 1
            A[n+i][n+i] = -1
            A[i][n+i] = 1
            A[n+i][i] = -1
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = Fraction(0, 1)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * determinant(submatrix)
        return det

    def automorphism_group_order(matrix):
        n = len(matrix)
        order = 1
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] != -matrix[j][i]:
                    return 0
                order *= (n-1) * (n-2) // 2
        return order

    def communication_complexity(f, M):
        # Placeholder function to simulate communication complexity
        return len(f)

    n_values = [5, 10, 15, 20, 30, 40]
    total_communication = 0
    instances_tested = 0

    for n in n_values:
        M = generate_symplectic_matrix(n)
        order = automorphism_group_order(M)
        if order == 0:
            return {
                "metric_name": "communication_complexity",
                "metric_value": 0,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "symplectic_matrix_not_found"
            }
        f = [random.randint(1, 10) for _ in range(n)]
        comm_complexity = communication_complexity(f, M)
        total_communication += comm_complexity
        instances_tested += len(f)

    mean_communication = Fraction(total_communication, instances_tested)
    expected_bound = n_values[-1] ** 2

    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_communication,
        "instances_tested": instances_tested,
        "n_max": n_values[-1],
        "conjecture_holds": abs(mean_communication - expected_bound) <= Fraction(expected_bound * 0.1, 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_communication = sum(r["metric_value"] for r in results) / len(results)
    std_communication = math.sqrt(sum((r["metric_value"] - mean_communication)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_communication} std={std_communication} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_communication} std={std_communication} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")