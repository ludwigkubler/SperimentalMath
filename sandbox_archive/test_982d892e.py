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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mul(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return result

def gaussian_elimination(A, b):
    n = len(b)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(Augmented[k][i]))
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        factor = Augmented[i][i]
        if factor == 0:
            raise ValueError("No unique solution exists")
        for j in range(i, n + 1):
            Augmented[i][j] /= factor
        for k in range(n):
            if k != i and Augmented[k][i] != 0:
                factor = Augmented[k][i]
                for j in range(i, n + 1):
                    Augmented[k][j] -= factor * Augmented[i][j]
    x = [Augmented[i][n] for i in range(n)]
    return x

def matroid_rank_deficit(M, DNF_terms):
    groundset = set(range(len(M)))
    closure = groundset
    for term in DNF_terms:
        closure |= {i for i in range(len(M)) if M[i][term]}
    rank_M = len([x for x in M if any(x[j] for j in range(len(DNF_terms)))])
    rank_groundset_minus_closure = len([x for x in groundset - closure if any(x[j] for j in range(len(DNF_terms)))])
    return rank_M - rank_groundset_minus_closure

def generate_k_clique_dnf(n, k):
    DNF_terms = []
    for i in range(k):
        term = [random.randint(0, 1) for _ in range(n)]
        if sum(term) == 1:
            DNF_terms.append(term)
    return DNF_terms

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        S_n = random.randint(1, min(n * (n - 1) // 2, 100))  # Ensure poly(n) size
        DNF_terms = generate_k_clique_dnf(n, 3)
        M = [[random.randint(0, 1) for _ in range(len(DNF_terms))] for _ in range(n)]
        mu_M = matroid_rank_deficit(M, DNF_terms)
        total_metric_value += mu_M
        instances_tested += len(DNF_terms)

        if mu_M > math.log(n):
            conjecture_holds = False
            counterexample = f"n={n}, S(n)={S_n}, mu(M)={mu_M} > log({n})"

    return {
        "metric_name": "matroid_rank_deficit",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")