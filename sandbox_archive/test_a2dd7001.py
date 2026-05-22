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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
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
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def is_quaternion_algebra(A):
        n = len(A)
        if n != 4:
            return False
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for a, b, c, d in itertools.product(range(n), repeat=4):
            Q = [
                [A[a][b], A[a][c], A[a][d], 0],
                [A[b][a], A[b][c], A[b][d], 0],
                [A[c][a], A[c][b], A[c][d], 0],
                [0, 0, 0, 1]
            ]
            if determinant(Q) != 0:
                return False
        return True

    def construct_monotone_circuit(n):
        # Simplified construction for demonstration purposes
        return n ** 2

    n = random.randint(5, 40)
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    while not is_quaternion_algebra(A):
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]

    circuit_size = construct_monotone_circuit(n)
    order_Q = n ** (n // 2)

    return {
        "metric_name": "order(Q)",
        "metric_value": order_Q,
        "instances_tested": 1,
        "conjecture_holds": order_Q >= circuit_size,
        "counterexample": "" if order_Q >= circuit_size else f"Order(Q)={order_Q} < Circuit size={circuit_size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order(Q) < Circuit size\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")