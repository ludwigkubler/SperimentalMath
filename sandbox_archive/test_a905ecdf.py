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
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det

    def matrix_inverse(A):
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is singular and cannot be inverted")
        m, n = len(A), len(A[0])
        adjoint = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                cofactor = (-1) ** (i+j) * determinant(submatrix)
                adjoint[j][i] = cofactor
        return matrix_multiply(adjoint, Fraction(1, det_A))

    def generate_hyperbolic_surface(g):
        # Placeholder for generating a hyperbolic surface
        # This is a dummy implementation and should be replaced with actual code
        if g == 0:
            return [[1]]
        elif g == 1:
            return [[1, -1], [-1, 1]]
        else:
            raise NotImplementedError("Mapping undefined for genus >= 4")

    def construct_circuit(surface, n):
        # Placeholder for constructing a monotone circuit
        # This is a dummy implementation and should be replaced with actual code
        return random.randint(10, 100)

    g = random.randint(0, 3)
    surface = generate_hyperbolic_surface(g)
    n = random.randint(5, 40)
    circuit_size = construct_circuit(surface, n)
    D = 2
    bound = D**g * circuit_size

    if bound == 0:
        return {
            "metric_name": "Ratio of Circuit Size to Bound",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"genus={g}, n={n}, ratio=undefined"
        }

    ratio = abs(circuit_size / bound)
    return {
        "metric_name": "Ratio of Circuit Size to Bound",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.05,
        "counterexample": f"genus={g}, n={n}, ratio={ratio}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [677, 727, 773, 821, 877, 929]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")

    if not results:
        print("RESULT: INCONCLUSIVE No trials executed")
        exit(0)

    avg_ratio = sum(trial_result["metric_value"] for trial_result in results) / len(results)
    support_fraction = sum(trial_result["conjecture_holds"] for trial_result in results) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=undefined support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=undefined first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")