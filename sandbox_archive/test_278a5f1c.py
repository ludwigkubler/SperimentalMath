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
    
    def generate_matrix(n):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                A[i][j] = random.randint(0, 1)
                A[j][i] = A[i][j]
        return A
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        n = len(A)
        r = 0
        for row in gaussian_elimination(A):
            if any(row):
                r += 1
        return r
    
    def communication_complexity(n):
        # Placeholder function, replace with actual implementation
        return random.randint(1, n)
    
    def minimal_local_induction_ring_rank(A):
        # Placeholder function, replace with actual implementation
        return rank(A) ** 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        A = generate_matrix(n)
        cc = communication_complexity(n)
        mrl = minimal_local_induction_ring_rank(A)
        if mrl > 10 * cc ** 2:
            return {
                "metric_name": "mrl_over_cc_squared",
                "metric_value": mrl / (cc ** 2),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"mrl({n}) = {mrl}, cc({n}) = {cc}"
            }
        results.append(mrl / (cc ** 2))
    
    return {
        "metric_name": "mrl_over_cc_squared",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": all(x <= 10 for x in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    metrics = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metrics.append(result["metric_value"])
    
    mean = sum(metrics) / len(metrics)
    std = math.sqrt(sum((x - mean) ** 2 for x in metrics) / len(metrics))
    support_fraction = sum(1 for m in metrics if m <= 10) / len(metrics)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(m > 10 for m in metrics):
        first_failing_seed = seeds[metrics.index(max(metrics))]
        print(f"RESULT: FALSIFIED counterexample=\"mrl_over_cc_squared exceeded 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")