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
    
    def generate_cnf(n: int) -> list:
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c != -d for c, d in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses

    def tensor_product(A: list, B: list) -> list:
        n = len(A)
        m = len(B)
        result = [[0] * (m * n) for _ in range(n * m)]
        for i in range(n):
            for j in range(m):
                for k in range(n):
                    for l in range(m):
                        result[i * m + j][k * m + l] += A[i][k] * B[j][l]
        return result

    def minimal_representation_dimension(cnf: list, n: int) -> int:
        if not cnf:
            return 0
        max_dim = 1
        for clause in cnf:
            dim = len(clause)
            A = [[0] * dim for _ in range(dim)]
            for i in range(dim):
                for j in range(dim):
                    A[i][j] = int(clause[i] == -clause[j])
            while True:
                try:
                    inv_A = gaussian_elimination(A, dim)
                    break
                except ZeroDivisionError:
                    dim += 1
                    A.append([0] * dim)
                    for row in A:
                        row.append(0)
            max_dim = max(max_dim, dim)
        return max_dim

    def gaussian_elimination(matrix: list, n: int) -> list:
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for i in range(n):
            pivot_row = i
            for j in range(i + 1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[pivot_row][i]):
                    pivot_row = j
            augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n + 1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[n:] for row in augmented_matrix]

    max_dim = 0
    instances_tested = 0
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            dim = minimal_representation_dimension(cnf, n)
            max_dim = max(max_dim, dim)
            instances_tested += 1

    conjecture_holds = max_dim <= n * math.log(n) if n > 1 else True
    counterexample = "" if conjecture_holds else f"n={n}, dim={max_dim}"
    
    return {
        "metric_name": "minimal_representation_dimension",
        "metric_value": max_dim,
        "instances_tested": instances_tested,
        "n_max": max_dim,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")