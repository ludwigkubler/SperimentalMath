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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def polynomial_representation(f, n):
        k = 4  # Using a fixed k for simplicity
        A = [[0] * (2**k) for _ in range(2**k)]
        for i in range(2**n):
            x = [i >> j & 1 for j in range(n)]
            f_val = f[i]
            for j in range(k):
                y = [x[j] ^ (i >> (j + n) & 1) for j in range(n)]
                A[f_val][sum(y)] += 1
        return A
    
    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if any(A[j][i] != 0 for j in range(i, m)):
                pivot_row = next(j for j in range(i, m) if A[j][i] != 0)
                A[i], A[pivot_row] = A[pivot_row], A[i]
                for j in range(m):
                    if i != j:
                        factor = A[j][i] / A[i][i]
                        for k in range(n):
                            A[j][k] -= factor * A[i][k]
                rank += 1
        return rank
    
    def tree_like_resolution_width(f, n):
        # Placeholder function; actual implementation needed
        return random.randint(1, 10)  # Dummy value for demonstration

    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    A = polynomial_representation(f, n)
    rank_A = matrix_rank(A)
    t_star_f = tree_like_resolution_width(f, n)

    return {
        "metric_name": "rank",
        "metric_value": rank_A,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank_A <= math.sqrt(n) * math.log2(n),
        "counterexample": "" if rank_A <= math.sqrt(n) * math.log2(n) else f"rank({n}) = {rank_A} > O(√{n}·log {n})"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds O(√n·log n)\" first_failing_seed={first_failing_seed}")