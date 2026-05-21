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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if rank < n and A[i][i] == 0:
            pivot_found = False
            for k in range(i, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    pivot_found = True
                    break
            if not pivot_found:
                continue
        if A[i][i] == 0:
            continue
        rank += 1
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = -A[k][i] / A[i][i]
                for j in range(i, n):
                    A[k][j] += factor * A[i][j]
    return rank

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))

def persistence_entropy(M):
    n = len(M)
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            distances.append(hamming_distance(M[i], M[j]))
    if not distances:
        return 0
    L = sum(distances)
    P = [d / L for d in distances]
    PE = -sum(p * math.log2(p) for p in P)
    return PE

def rank_real(M):
    M_copy = [row[:] for row in M]
    rank = gaussian_elimination(M_copy)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 16, 24, 32])
    family = random.randint(0, 4)

    if family == 0:  # i.i.d. Bernoulli ±1
        M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    elif family == 1:  # sign(AB^T) with A,B Gaussian of inner rank r ∈ {1,2,4,8}
        r = random.choice([1, 2, 4, 8])
        A = [[random.gauss(0, 1) for _ in range(r)] for _ in range(n)]
        B = [[random.gauss(0, 1) for _ in range(n)] for _ in range(r)]
        M = [[sum(a * b for a, b in zip(A[i], B[j])) for j in range(n)] for i in range(n)]
    elif family == 2:  # Sylvester–Hadamard for n ∈ {8,16,32}
        if n not in [8, 16, 32]:
            return {"metric_name": "PE", "metric_value": -math.inf, "instances_tested": 0, "conjecture_holds": False, "counterexample": "mapping_undefined"}
        M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    elif family == 3:  # random ±1 circulants
        M = [[M[i - j % n][j] for j in range(n)] for i in range(n)]
    else:  # row-repeated Hadamard blocks (forced low-rank, wide distance spread — the natural adversary)
        block_size = n // 4
        M = []
        for _ in range(4):
            block = [[random.choice([-1, 1]) for _ in range(block_size)] for _ in range(block_size)]
            M.extend(block)

    PE = persistence_entropy(M)
    rank = rank_real(M)
    if 2 ** PE > rank + 1:
        return {"metric_name": "PE", "metric_value": PE, "instances_tested": 1, "conjecture_holds": False, "counterexample": f"2^PE({PE}) > rank+1({rank+1})"}
    else:
        return {"metric_name": "PE", "metric_value": PE, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_PE = sum(result["metric_value"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    std_PE = math.sqrt(sum((result["metric_value"] - mean_PE)**2 * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_PE} std={std_PE} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        worst_slack = min(result["metric_value"] * result["instances_tested"] for result in results)
        print(f"RESULT: FALSIFIED counterexample=\"2^PE > rank+1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")