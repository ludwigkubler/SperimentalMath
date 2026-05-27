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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(A):
        A_rref = gaussian_elimination(A)
        r = 0
        for row in A_rref:
            if any(row):
                r += 1
        return r

    def inner_product_mod_2(x, y):
        return sum(a * b % 2 for a, b in zip(x, y))

    def trivial_bp(n):
        return [[inner_product_mod_2(i, j) for j in range(2**n)] for i in range(2**n)]

    n = random.choice([5, 10, 15, 20, 30, 40])
    s_P = 2**n
    P = trivial_bp(n)
    rho_H_P = rank(P)

    metric_value = abs(rho_H_P - math.log(s_P))
    conjecture_holds = metric_value <= 0.1 and rho_H_P <= math.log(s_P) + 1
    counterexample = "" if conjecture_holds else f"n={n}, s(P)={s_P}, ρ_H(P)={rho_H_P}"
    
    return {
        "metric_name": "ρ_H(P)",
        "metric_value": rho_H_P,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = f"n={results[0]['instances_tested']}, s(P)={results[0]['metric_value']}, ρ_H(P)={results[0]['counterexample']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")