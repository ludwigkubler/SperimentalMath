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
    q = 2  # Example finite field F_q, can be changed to other primes if needed
    n = random.randint(5, 40)
    instances_tested = 100  # Ensure at least 30 instances per seed for statistical signal

    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges

    def characteristic_polynomial(matrix):
        det = 0
        sign = 1
        for p in itertools.permutations(range(n)):
            term = sign * matrix[p[0]][p[0]]
            for i in range(1, n):
                term *= matrix[p[i]][p[(i + p[0]) % n]]
            det += term
            sign *= -1
        return det

    def gram_schmidt(matrix):
        q = len(matrix)
        rank = 0
        for i in range(q):
            if any(matrix[j][i] != 0 for j in range(i)):
                rank += 1
                matrix[i][:] = [matrix[i][j] / matrix[i][i] for j in range(q)]
                for j in range(i + 1, q):
                    matrix[j][:] = [matrix[j][k] - matrix[j][i] * matrix[i][k] for k in range(q)]
        return rank

    def sum_of_squares_degree(n):
        # Placeholder function, replace with actual implementation
        return n

    total_rank = 0
    total_sum_of_squares = 0

    for _ in range(instances_tested):
        max_cut_instance = generate_max_cut_instance(n)
        matrix = [[random.randint(0, q - 1) for _ in range(n)] for _ in range(n)]
        det = characteristic_polynomial(matrix)
        rank = gram_schmidt(matrix)
        sum_of_squares = sum_of_squares_degree(n)

        total_rank += rank
        total_sum_of_squares += sum_of_squares

    avg_rank = total_rank / instances_tested
    avg_sum_of_squares = total_sum_of_squares / instances_tested

    conjecture_holds = avg_rank >= avg_sum_of_squares
    counterexample = "" if conjecture_holds else f"avg_rank={avg_rank}, avg_sum_of_squares={avg_sum_of_squares}"

    return {
        "metric_name": "Rank vs Sum-of-Squares Degree",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"avg_rank < avg_sum_of_squares\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")