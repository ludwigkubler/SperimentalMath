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
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank_variance(matrix):
        m, n = len(matrix), len(matrix[0])
        I = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        A = matrix_multiply(gaussian_elimination(matrix), I)
        rank = sum(1 for row in A if any(row))
        return (m * n - rank ** 2) / (m * n)

    def geometric_flow_invariant(matrix):
        m, n = len(matrix), len(matrix[0])
        flow = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if matrix[i][j]:
                    flow[i][(j + 1) % n] += 1
        return sum(abs(flow[i][j]) for i in range(m) for j in range(n))

    def generate_protocol(n):
        protocol = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2 ** n)]
        return protocol

    k = 0.5  # Threshold value
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            protocol = generate_protocol(n)
            rv = rank_variance(protocol)
            mfi = geometric_flow_invariant(protocol)
            instances_tested += 1
            n_max = max(n_max, n)
            if abs(mfi - rv) > k:
                conjecture_holds = False
                counterexample = f"Protocol with n={n} failed. MFI: {mfi}, RV: {rv}"
                break

    return {
        "metric_name": "MFI_RV_Difference",
        "metric_value": abs(mfi - rv),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")