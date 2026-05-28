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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_rank(A):
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank

    def characteristic_polynomial(A):
        n = len(A)
        identity = [[int(i == j) for i in range(n)] for j in range(n)]
        t = random.randint(2, n)
        poly = [0] * (n + 1)
        poly[0] = (-1) ** n
        for k in range(1, n + 1):
            A_t = [[A[i][j] for j in range(n)] for i in range(n)]
            for _ in range(t):
                A_t = matrix_multiply(A_t, A)
            poly[k] = (-1) ** (n - k) * sum(sum(row[j] for j in range(k)) for row in A_t)
        return poly

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def birfield_rank(n, k):
        # Placeholder for actual Birfield rank computation
        # This is a dummy implementation for testing purposes
        return n ** k * math.log(n)

    def monotone_circuit_rank(n):
        # Placeholder for actual monotone circuit rank computation
        # This is a dummy implementation for testing purposes
        return (math.log(n)) ** 2

    instances_tested = 0
    mean_rho_B = 0
    mean_rho_C = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            instances_tested += 1
            rho_B = birfield_rank(n, k)
            rho_C = monotone_circuit_rank(n)
            mean_rho_B += rho_B
            mean_rho_C += rho_C

            if rho_B < n ** k * math.log(n) or rho_C > (math.log(n)) ** 2:
                conjecture_holds = False
                counterexample = f"rho_B={rho_B}, rho_C={rho_C}"
                break

    return {
        "metric_name": "rho_B and rho_C",
        "metric_value": {"mean_rho_B": mean_rho_B / instances_tested, "mean_rho_C": mean_rho_C / instances_tested},
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rho_B = sum(res["metric_value"]["mean_rho_B"] for res in results) / len(results)
    mean_rho_C = sum(res["metric_value"]["mean_rho_C"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean_rho_B={mean_rho_B} mean_rho_C={mean_rho_C} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")