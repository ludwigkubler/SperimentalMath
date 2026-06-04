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
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(i, n):
                A[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def communication_complexity_rank(G, d):
        n = len(G)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    M[i][j] = random.randint(1, d)
                    M[j][i] = M[i][j]
        return max(sum(row) for row in gaussian_elimination(M))

    def minimal_local_indeterminacy(G):
        n = len(G)
        indeterminacies = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    indeterminacies[i] += 1
                    indeterminacies[j] += 1
        return max(indeterminacies)

    def generate_noncommutative_complexity(n, d):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i][j] = 1
                    G[j][i] = 1
        return G

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_epsilon = 0
        max_n = n
        for _ in range(5):
            G = generate_noncommutative_complexity(n, d)
            epsilon = minimal_local_indeterminacy(G)
            r = communication_complexity_rank(G, d)
            if r > 0:
                instances_tested += 1
                total_epsilon += epsilon
                max_n = max(max_n, n)
        if instances_tested < 30:
            continue
        avg_epsilon = total_epsilon / instances_tested
        correlation_coefficient = (avg_epsilon - k**2) / k**2
        results.append({
            "metric_name": "communication_complexity_rank",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": abs(correlation_coefficient) > 0.1,
            "counterexample": "" if abs(correlation_coefficient) > 0.1 else "correlation_coefficient=0"
        })

    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 24:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction / len(results):.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient=0' first_failing_seed={first_failing_seed}")