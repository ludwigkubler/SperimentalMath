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

def generate_matroid(n, r):
    if r == 0:
        return []
    elif r == n:
        return [[i for i in range(n)]]
    else:
        base = random.sample(range(n), r)
        matroid = [base]
        while len(matroid) < n - r + 1:
            new_element = random.randint(0, n-1)
            if all(new_element not in H for H in matroid):
                matroid.append([new_element] + H for H in matroid)
        return matroid

def encode_matroid(matroid):
    n = len(matroid[0])
    encoding = [0] * (n * n)
    for H in matroid:
        for i in H:
            encoding[i * n + i] = 1
    return ''.join(str(bit) for bit in encoding)

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for j in range(n):
        pivot_row = -1
        for i in range(rank, m):
            if matrix[i][j] == 1:
                pivot_row = i
                break
        if pivot_row != -1:
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for i in range(m):
                if i != rank and matrix[i][j] == 1:
                    for k in range(n):
                        matrix[i][k] ^= matrix[rank][k]
            rank += 1
    return rank

def compute_circuit_size(matroid, q):
    n = len(matroid[0])
    encoding_size = (n * n).bit_length()
    rank = gaussian_elimination(matroid)
    if q == 2:
        circuit_size = encoding_size + rank * math.log2(n) * 2
    else:
        circuit_size = float('inf')
    return circuit_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(100):
            matroid = generate_matroid(n, random.randint(1, min(n-1, 4)))
            s_M = (n * n).bit_length()
            q = 2
            circuit_size = compute_circuit_size(matroid, q)
            if circuit_size > s_M * (n ** 0.5):
                conjecture_holds = False
                counterexample = f"Matroid of rank {len(matroid)} with n={n}"
                break
            total_metric_value += circuit_size
            instances_tested += 1

    return {
        "metric_name": "circuit_size",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
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
        print("RESULT: INCONCLUSIVE mapping_undefined")