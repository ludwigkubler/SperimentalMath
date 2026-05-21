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

def gaussian_elimination(A, p):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = -A[i][i] % p
        for j in range(n):
            A[i][j] = (A[i][j] * factor) % p
        for j in range(n):
            if i != j:
                factor = A[j][i] % p
                for k in range(n):
                    A[j][k] = (A[j][k] - factor * A[i][k]) % p

def rank_nc(A, p):
    n = len(A)
    rank = 0
    gaussian_elimination(A, p)
    for i in range(n):
        if A[i][i] != 0:
            rank += 1
    return rank

def generate_bp(n, read_twice=False):
    bp = []
    for _ in range(n):
        if read_twice:
            access = random.sample(range(2), 2)
        else:
            access = [random.randint(0, 1)]
        bp.append(access)
    return bp

def tensor_product(bp1, bp2):
    n1 = len(bp1)
    n2 = len(bp2)
    result = [[[] for _ in range(n2)] for _ in range(n1)]
    for i in range(n1):
        for j in range(n2):
            for a in bp1[i]:
                for b in bp2[j]:
                    result[i][j].append((a, b))
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    p = 23  # Prime number for modulo operation
    instances_tested = 0
    total_rank = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(10):  # Test with 10 random read-once and read-twice BPs
        bp1 = generate_bp(n, False)
        bp2 = generate_bp(n, True)
        M = tensor_product(bp1, bp2)
        rank = rank_nc(M, p)
        instances_tested += 1
        total_rank += rank

    avg_rank = total_rank / instances_tested
    if read_twice:
        if avg_rank <= math.log(n, 2):
            conjecture_holds = False
            counterexample = "Read-twice BP has noncommutative rank ≤ log n"
    else:
        if avg_rank > math.log(n, 2):
            conjecture_holds = False
            counterexample = "Read-once BP has noncommutative rank > log n"

    return {
        "metric_name": "Noncommutative Rank",
        "metric_value": avg_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")