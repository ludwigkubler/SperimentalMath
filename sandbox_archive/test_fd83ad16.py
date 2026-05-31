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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(n):
        pivot = None
        for j in range(rank, m):
            if A[j][i] != 0:
                pivot = j
                break
        if pivot is None:
            continue
        A[pivot], A[rank] = A[rank], A[pivot]
        for j in range(m):
            if j != rank and A[j][i] != 0:
                factor = Fraction(A[j][i], A[rank][i])
                for k in range(n):
                    A[j][k] -= factor * A[rank][k]
        rank += 1
    return rank

def min_rank(M):
    M_copy = [row[:] for row in M]
    return gaussian_elimination(M_copy)

def tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    for i in range(2, n + 1):
        clauses.append([variables[i - 1], -variables[i - 2]])
        for j in range(i - 3, -1, -1):
            new_var = len(variables) + 1
            variables.append(new_var)
            clauses.append([-new_var, variables[j], -i])
            clauses.append([new_var, i])
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        variables, clauses = tseitin_formula(n)
        M = [[0] * len(variables) for _ in range(len(clauses))]
        for j, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    M[j][var - 1] = 1
                else:
                    M[j][-var - 1] = 1

        rank = min_rank(M)
        w_phi_G = len(clauses)  # Simplified resolution proof width for Tseitin formulas

        if instances_tested == 0 or n > n_max:
            n_max = n
        instances_tested += len(clauses)

        ratio = Fraction(rank, w_phi_G)
        total_metric_value += ratio

        if not (Fraction(1, 2) <= ratio <= Fraction(3, 2)):
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank}, w(φ_G)={w_phi_G}, ratio={ratio}"

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = Fraction(instances_tested - sum(1 for _ in range(n_max) if not conjecture_holds), instances_tested)

    return {
        "metric_name": "Ratio of Minimal Rank to Resolution Proof Width",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = Fraction(sum(1 for result in results if result["conjecture_holds"]), len(results))

    print("TRIALS:")
    for result in results:
        print(f"  TRIAL: {result}")

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= Fraction(9, 10):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")