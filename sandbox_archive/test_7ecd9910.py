# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    def random_3sat_instance(n: int, m: int) -> list:
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            clauses.append(clause)
        return clauses

    def matrix_from_3sat(instance: list, n: int) -> list:
        matrix = [[0] * n for _ in range(n)]
        for clause in instance:
            for var in clause:
                if var > 0:
                    matrix[var - 1][var - 1] += 1
                else:
                    matrix[-var - 1][-var - 1] -= 1
        return matrix

    def determinant(matrix: list) -> int:
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** (j % 2)
            det += sign * matrix[0][j] * determinant(submatrix)
        return det

    def permanent(matrix: list) -> int:
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        perm = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** (j % 2)
            perm += sign * matrix[0][j] * permanent(submatrix)
        return abs(perm)

    def count_partition_occurrences(matrix, partition):
        n = len(matrix)
        if n != len(partition):
            return 0
        count = 0
        for perm in set(permutations(range(n))):
            product = 1
            for i, p in enumerate(perm):
                product *= matrix[i][p]
            if sorted([product] * partition[i]) == sorted(matrix):
                count += 1
        return count

    def permutations(lst):
        if len(lst) == 0:
            return []
        if len(lst) == 1:
            return [lst]
        l = []
        for i in range(len(lst)):
           m = lst[i]
           remLst = lst[:i] + lst[i+1:]
           for p in permutations(remLst):
               l.append([m] + p)
        return l

    n = random.randint(5, 40)
    m = random.randint(3 * n, 6 * n)
    instance = random_3sat_instance(n, m)
    matrix = matrix_from_3sat(instance, n)

    det_value = determinant(matrix)
    perm_value = permanent(matrix)

    det_partition_count = count_partition_occurrences(matrix, [n])
    perm_partition_count = count_partition_occurrences(matrix, [n])

    metric_name = "partition_count_difference"
    metric_value = perm_partition_count - det_partition_count
    instances_tested = 1
    conjecture_holds = metric_value >= math.sqrt(n)
    counterexample = "" if conjecture_holds else f"Partition count difference {metric_value} < sqrt({n})"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + list(map(lambda p: int(p), primes(40)))
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Partition count difference < sqrt(n)\" first_failing_seed={first_failing_seed}")

def primes(n):
    sieve = [True] * (n+1)
    for x in range(2, int(n**0.5) + 1):
        if sieve[x]:
            for i in range(x*x, n+1, x):
                sieve[i] = False
    return [x for x in range(2, n+1) if sieve[x]]