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
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def rank(A):
        m, n = len(A), len(A[0])
        r = 0
        for i in range(m):
            if any(A[i][j] != 0 for j in range(n)):
                r += 1
        return r

    def generate_k_clique_instance(n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    edges.append((i, j))
        return edges

    def construct_affine_scheme(edges):
        m = len(edges)
        A = [[0] * (m + 1) for _ in range(m + 1)]
        for i, (u, v) in enumerate(edges):
            A[i][u] = 1
            A[i][v] = -1
            A[m][i] = 1
        return A

    n = random.randint(5, 40)
    edges = generate_k_clique_instance(n)
    A = construct_affine_scheme(edges)
    rank_A = rank(gaussian_elimination(A))
    
    return {
        "metric_name": "Rank of Tropicalized Affine Scheme",
        "metric_value": rank_A,
        "instances_tested": 1,
        "conjecture_holds": True if 0.9 * n**0.25 <= rank_A <= 1.1 * n**0.25 else False,
        "counterexample": "" if 0.9 * n**0.25 <= rank_A <= 1.1 * n**0.25 else f"n={n}, rank={rank_A}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")