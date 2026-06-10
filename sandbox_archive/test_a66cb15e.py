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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
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

    def matrix_rank(A):
        rank = 0
        A_rref = gaussian_elimination(A)
        for row in A_rref:
            if any(row):
                rank += 1
        return rank

    def generate_protocol(n):
        protocol = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return protocol

    def compute_rank_variance(protocol):
        n = len(protocol)
        mean = sum(sum(row) for row in protocol) / (n * n)
        variance = sum((sum(row) - mean) ** 2 for row in protocol) / (n * n)
        return variance

    def lie_algebroid_cohomology_rank(protocol):
        n = len(protocol)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if protocol[i][j]:
                    A[i][j] = 1
        return matrix_rank(A)

    def communication_complexity(rank):
        return math.sqrt(rank) * n

    n_max = 0
    instances_tested = 0
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        n_max = max(n_max, n)
        protocol = generate_protocol(n)
        rank_variance = compute_rank_variance(protocol)
        cohomology_rank = lie_algebroid_cohomology_rank(protocol)
        communication_complexity_value = communication_complexity(cohomology_rank)

        if cohomology_rank < math.sqrt(rank_variance):
            conjecture_holds = False
            counterexample = f"Protocol with n={n}, rank variance {rank_variance}, cohomology rank {cohomology_rank} violates the conjecture."

        total_metric_value += cohomology_rank
        instances_tested += 1

    return {
        "metric_name": "Lie algebroid cohomology rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
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

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")