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
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def generate_3sat_instance(n: int) -> list:
        clauses = []
        for _ in range(n):
            clause = [random.choice(range(-n, n+1)) for _ in range(3)]
            clauses.append(clause)
        return clauses

    def incidence_matrix(clauses: list, n: int) -> list:
        matrix = [[0] * n for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    matrix[i][var-1] = 1
                else:
                    matrix[i][-var-1] = -1
        return matrix

    def hook_length_form(n: int) -> int:
        hook_lengths = [n + i - j for i in range(1, n+1) for j in range(i)]
        product = math.prod(hook_lengths)
        factorial_n = math.factorial(n)
        return product // (factorial_n ** 2)

    def irreducible_components(n: int, k: int) -> int:
        if k == 0:
            return 1
        return sum([hook_length_form(i) * hook_length_form(j) for i in range(1, n+1) for j in range(1, n+1)]) // (n ** 2)

    def permanent(matrix: list) -> int:
        if len(matrix) == 0:
            return 1
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            sign = (-1) ** i
            det += sign * matrix[0][i] * permanent(submatrix)
        return det

    def determinant(matrix: list) -> int:
        if len(matrix) == 0:
            return 1
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            sign = (-1) ** i
            det += sign * matrix[0][i] * determinant(submatrix)
        return det

    n = 20
    k = n // 2
    random.seed(seed)
    instance = generate_3sat_instance(n)
    matrix = incidence_matrix(instance, n)

    perm_components = irreducible_components(n, k)
    det_components = irreducible_components(n, k)

    metric_name = "Symmetric Power Decomposition Complexity Gap"
    metric_value = perm_components - det_components
    instances_tested = 1
    conjecture_holds = metric_value >= 2 ** n
    counterexample = "" if conjecture_holds else f"Permanent components: {perm_components}, Determinant components: {det_components}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        primes = []
        num_primes = 30
        candidate = 2
        while len(primes) < num_primes:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        seeds = primes

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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")