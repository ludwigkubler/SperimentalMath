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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def rank(A):
        A = [row[:] for row in A]
        r = gaussian_elimination(A)
        return sum(1 for row in r if any(x != 0 for x in row))

    def generate_protocol(n):
        protocol = []
        for _ in range(n):
            protocol.append(random.randint(0, n-1))
        return protocol

    def rank_variance(protocol):
        n = len(protocol)
        mean = sum(protocol) / n
        variance = sum((x - mean) ** 2 for x in protocol) / n
        return variance

    def construct_affine_plane(n):
        points = set()
        for i in range(n):
            for j in range(n):
                if (i, j) not in points:
                    points.add((i, j))
        return list(points)

    def projective_representation(plane, protocol):
        n = len(plane)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if (i, j) in plane:
                    M[i][j] = 1
        return M

    def communication_complexity(M):
        m, n = len(M), len(M[0])
        rank_M = rank(M)
        return rank_M ** 2

    n = random.randint(5, 40)
    protocol = generate_protocol(n)
    variance = rank_variance(protocol)
    plane = construct_affine_plane(n)
    M = projective_representation(plane, protocol)
    comm_complexity = communication_complexity(M)

    metric_value = len(plane) / (variance ** 2)
    conjecture_holds = metric_value <= 3 * (len(plane) // variance ** 2)
    counterexample = "" if conjecture_holds else f"n={n}, protocol={protocol}, plane_size={len(plane)}, variance={variance}"
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")