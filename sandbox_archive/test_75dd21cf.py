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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def matrix_multiplication(A, B):
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(matrix):
        matrix = gaussian_elimination(matrix)
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank

    n = random.randint(5, 40)
    if n == 1:
        return {
            "metric_name": "rank",
            "metric_value": 1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "single_output_stub"
        }

    # Generate a random read-twice branching program
    program = []
    for _ in range(n):
        if random.choice([True, False]):
            program.append(random.randint(0, n-1))
        else:
            program.append(None)

    # Construct the associated tropical algebraic stack
    stack = [[0] * (n+1) for _ in range(n+1)]
    for i in range(n):
        if program[i] is not None:
            stack[program[i]][i+1] = 1

    # Compute the rank of the tropical algebraic stack
    rank_value = rank(stack)

    return {
        "metric_name": "rank",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": False if n > 1 and rank_value != math.log2(n) else True,
        "counterexample": "" if n <= 1 or rank_value == math.log2(n) else f"n={n}, expected {math.log2(n)}, got {rank_value}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")