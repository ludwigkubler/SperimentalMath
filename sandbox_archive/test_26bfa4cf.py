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
from fractions import Fraction
import math

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = max(range(rank, m), key=lambda i: abs(A[i][j]))
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = -A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] += factor * A[rank][k]
        rank += 1
    return rank

def matrix_rank(A):
    return gaussian_elimination(A)

def random_kcnf(n, m, k):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < k:
            var = random.choice(variables)
            if -var not in clause:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def projective_space_embedding(cnf):
    n = max(abs(x) for x in cnf)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for literal in cnf:
        i = abs(literal)
        if literal > 0:
            A[i][i] += 1
        else:
            A[-i][-i] += 1
    return matrix_rank(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    min_sym_vol = float('inf')
    comm_rank_variance = 0.0

    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            k = random.randint(2, min(3, n))
            cnf = random_kcnf(n, m, k)
            sym_vol = projective_space_embedding(cnf)
            comm_rank = matrix_rank([list(x) for x in cnf])
            instances_tested += 1
            if sym_vol < min_sym_vol:
                min_sym_vol = sym_vol
            comm_rank_variance += comm_rank ** 2

    if instances_tested < 30:
        return {
            "metric_name": "Minimal Symplectic Volume to Communication Complexity Rank Variance Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }

    comm_rank_variance /= instances_tested
    ratio = abs(Fraction(min_sym_vol, comm_rank_variance))

    return {
        "metric_name": "Minimal Symplectic Volume to Communication Complexity Rank Variance Ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": ratio <= 10,  # Placeholder constant for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")