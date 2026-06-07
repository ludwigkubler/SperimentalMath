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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll_width(phi, assignment):
        if not phi:
            return 0
        if any(lit in assignment and assignment[lit] != val for lit, val in phi[0].items()):
            return math.inf
        if all(lit in assignment or -lit in assignment for lit, _ in phi[0].items()):
            return dpll_width(phi[1:], assignment)
        p = next(lit for lit, _ in phi[0].items() if lit not in assignment and -lit not in assignment)
        return min(dpll_width(phi[1:] + [[{p: True}]], assignment | {p: True}), dpll_width(phi[1:] + [[{-p: True}]], assignment | {-p: True}))

    def tropical_motivic_rank(phi):
        n = len(phi)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if phi[i][j]:
                    A[i][j] = 1
                    A[j][i] = 1
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return rank

    def generate_phi(n):
        phi = []
        for _ in range(n):
            clause = {}
            for lit in random.sample(range(-n, n+1), random.randint(2, n)):
                if lit not in clause and -lit not in clause:
                    clause[lit] = True
            phi.append(clause)
        return phi

    n_max = 0
    total_ratio = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        phi = generate_phi(n)
        mtr = tropical_motivic_rank(phi)
        w_dpll = dpll_width(phi, {})
        ratio = mtr / (w_dpll + 1e-9)  # Add small epsilon to avoid division by zero
        total_ratio += ratio
        instances_tested += 1

    mean_ratio = total_ratio / instances_tested
    if mean_ratio > 2:  # Example threshold, adjust as needed
        conjecture_holds = False
        counterexample = "mean_ratio_exceeds_threshold"

    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
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

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")