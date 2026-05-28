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
import math
from fractions import Fraction

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = matrix[i][i]
        if factor == 0:
            return None  # Matrix is not full rank
        for j in range(i, cols):
            matrix[i][j] /= factor
        for j in range(rows):
            if j != i:
                factor = matrix[j][i]
                for k in range(i, cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return sum(1 for row in matrix if any(row))

def barratt_floer_homology(f):
    N = len(f)
    H = [[0] * (N + 1) for _ in range(N)]
    for i in range(N):
        H[i][i] = f[i]
    rank = gaussian_elimination(H)
    return rank

def xor_circuit_size(n):
    if n == 1:
        return 1
    return 2 * xor_circuit_size(n // 2) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_ratio = 0
        max_ratio = 0
        for _ in range(30):
            f = {i: random.choice([-1, 1]) for i in range(n)}
            rank = barratt_floer_homology(f)
            if rank is None:
                continue
            circuit_size = xor_circuit_size(n)
            ratio = circuit_size / (2 ** (rank + 1))
            instances_tested += 1
            total_ratio += ratio
            max_ratio = max(max_ratio, ratio)
        if instances_tested == 0:
            continue
        avg_ratio = total_ratio / instances_tested
        conjecture_holds = avg_ratio >= 2 ** (rank + 1) and max_ratio <= 2 ** (math.log(n, 2) + 1)
        counterexample = "" if conjecture_holds else f"avg_ratio={avg_ratio}, max_ratio={max_ratio}"
        results.append({
            "n": n,
            "instances_tested": instances_tested,
            "avg_ratio": avg_ratio,
            "max_ratio": max_ratio,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    metric_value = sum(result["avg_ratio"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    return {
        "metric_name": "average ratio",
        "metric_value": metric_value,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"avg_ratio too low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")