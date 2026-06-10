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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r

    def generate_protocol(n):
        protocol = [random.randint(0, 1) for _ in range(n)]
        return protocol

    def moduli_space(protocol):
        n = len(protocol)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            M[i][i] = 1
            M[n][i] = protocol[i]
        return M

    def hcr(M):
        return rank(M)

    def rvar(protocol):
        n = len(protocol)
        mean = sum(protocol) / n
        variance = sum((x - mean) ** 2 for x in protocol) / n
        return variance

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        hcr_sum = 0
        rvar_sum = 0
        for _ in range(5):
            protocol = generate_protocol(n)
            M = moduli_space(protocol)
            hcr_val = hcr(M)
            rvar_val = rvar(protocol)
            instances_tested += 1
            hcr_sum += hcr_val
            rvar_sum += rvar_val
        if instances_tested < 5:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        hcr_avg = hcr_sum / instances_tested
        rvar_avg = rvar_sum / instances_tested
        correlation = (instances_tested * sum(hcr_val * rvar_val for hcr_val, rvar_val in zip(results, results)) -
                       sum(results) * sum(results)) / math.sqrt((instances_tested * sum(hcr_val ** 2 for hcr_val in results) - sum(results) ** 2) *
                                                            (instances_tested * sum(rvar_val ** 2 for rvar_val in results) - sum(results) ** 2))
        results.append(correlation)
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")