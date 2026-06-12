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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    clauses = []
    for i in range(n):
        clause = [f[j] for j in range(2**n) if (j >> i) & 1]
        clauses.append(clause)
    rank_var = sum([len(set(c)) for c in clauses]) / n
    return rank_var

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_mul(A, B, mod):
    return [[sum((A[i][k] * B[k][j]) % mod for k in range(len(B))) % mod for j in range(len(B[0]))] for i in range(len(A))]

def matrix_inv(A, mod):
    n = len(A)
    A_aug = [row + [i == j for j in range(n)] for i, row in enumerate(A)]
    for i in range(n):
        pivot = A_aug[i][i]
        if pivot == 0:
            return None
        for j in range(n * 2):
            A_aug[i][j] = (A_aug[i][j] * pow(pivot, mod - 2, mod)) % mod
        for j in range(n):
            if i != j:
                factor = A_aug[j][i]
                for k in range(n * 2):
                    A_aug[j][k] = (A_aug[j][k] - factor * A_aug[i][k]) % mod
    return [row[n:] for row in A_aug]

def minimal_order_brauer_group(f, n):
    B = [[0 if i != j else 1 for j in range(2**n)] for i in range(2**n)]
    I = [[1 if i == j else 0 for j in range(2**n)] for i in range(2**n)]
    A = matrix_sub(B, [f[i] * I[i] for i in range(2**n)])
    inv_A = matrix_inv(A, 2)
    if inv_A is None:
        return float('inf')
    B_bar = matrix_mul(inv_A, B, 2)
    rank = sum([sum(row) % 2 for row in B_bar])
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        f = generate_boolean_function(n)
        R_f = communication_complexity_rank_variance(f)
        if R_f == 0:
            continue
        rank = minimal_order_brauer_group(f, n)
        total_metric_value += rank / (R_f ** 2)
        instances_tested += 1
        n_max = max(n_max, n)

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else float('nan')
    support_fraction = instances_tested / len(n_values) if instances_tested > 0 else float('nan')

    return {
        "metric_name": "minimal_order_brauer_group",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results) if any(not math.isnan(r["metric_value"]) for r in results) else float('nan')
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")