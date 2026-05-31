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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(i, n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = Fraction(0)
        sign = Fraction(1, 1)
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -Fraction(1, 1)
        return det

    def is_symplectic_matrix(M):
        n = len(M)
        I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        J = [[Fraction(0, 1) if i == j else (Fraction(1, 1) if i + j == n - 1 else Fraction(0, 1)) for j in range(n)] for i in range(n)]
        return matrix_multiplication(matrix_multiplication(M, I), M) == J and matrix_multiplication(matrix_multiplication(I, M), M) == J

    def communication_complexity(f, M):
        n = len(M)
        if not is_symplectic_matrix(M):
            return float('inf')
        A = [[Fraction(0, 1)] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[i][j] = Fraction(f(i + 1, j + 1), 1)
        A = gaussian_elimination(A)
        det_A = determinant(A)
        return abs(det_A)

    def random_symplectic_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    M[i][j] = Fraction(1, 1)
                else:
                    M[i][j] = random.choice([Fraction(1, 1), -Fraction(1, 1)])
                    M[j][i] = Fraction(0, 1) if i + j != n - 1 else -M[i][j]
        return M

    def polynomial_evaluation(f, x):
        result = Fraction(0, 1)
        power = Fraction(1, 1)
        for coeff in f:
            result += coeff * power
            power *= x
        return result

    def random_polynomial(n):
        return [random.choice([Fraction(0, 1), Fraction(1, 1)]) for _ in range(n + 1)]

    n = 40
    instances_tested = 30
    communication_complexities = []
    
    for _ in range(instances_tested):
        M = random_symplectic_matrix(n)
        f = random_polynomial(n)
        comm_complexity = communication_complexity(f, M)
        if comm_complexity == float('inf'):
            continue
        communication_complexities.append(comm_complexity)

    if not communication_complexities:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "symplectic_matrix_not_found"
        }

    mean_comm = sum(communication_complexities) / len(communication_complexities)
    std_comm = math.sqrt(sum((x - mean_comm) ** 2 for x in communication_complexities) / len(communication_complexities))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": abs(mean_comm - n**2) <= 0.1 * n**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_comm = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_comm = math.sqrt(sum((r["metric_value"] - mean_comm) ** 2 for r in results if r["conjecture_holds"]) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm} std={std_comm} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm} std={std_comm} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")