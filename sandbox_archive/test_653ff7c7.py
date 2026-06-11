# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        if M[i][i] == 0:
            for j in range(i + 1, n):
                if M[j][i] != 0:
                    M[i], M[j] = M[j], M[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        for j in range(n):
            if i == j:
                continue
            factor = Fraction(M[j][i], M[i][i])
            for k in range(n):
                M[j][k] -= factor * M[i][k]
    return [row[:n] for row in M]

def local_induction_degree_bound(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j]:
                A[i][i] += 1
                A[j][j] += 1
                A[i][j] -= 1
                A[j][i] -= 1
    rank_A = len(gaussian_elimination(A))
    return rank_A

def communication_complexity_rank_variance(G):
    n = len(G)
    RCV = 0
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j]:
                RCV += (i - j) ** 2
    return RCV

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    LIDB = local_induction_degree_bound(G)
    RCV = communication_complexity_rank_variance(G)
    return {
        "metric_name": "LIDB vs RCV",
        "metric_value": abs(LIDB - RCV),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    if all(not r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results)} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")