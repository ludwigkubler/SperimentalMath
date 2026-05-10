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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = 1
    return M

def matrix_power(M, k):
    result = [[0] * len(M) for _ in range(len(M))]
    for i in range(len(M)):
        result[i][i] = 1
    for _ in range(k):
        temp = [[0] * len(M) for _ in range(len(M))]
        for i in range(len(M)):
            for j in range(len(M)):
                for k in range(len(M)):
                    temp[i][j] += M[i][k] * M[k][j]
        result = temp
    return result

def trace(M):
    return sum(M[i][i] for i in range(len(M)))

def schatten_p_norm(M, p):
    if p == 2:
        return math.sqrt(trace(matrix_power(M, 2)))
    else:
        M_k = matrix_power(M, int(math.log2(len(M)) + 1))
        return (trace(M_k) / len(M)) ** (1 / p)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    ratios = []
    for p in [2, 3, math.log2(n) + 1]:
        norm_p = schatten_p_norm(M, p)
        ratio = norm_p / (n ** (1/2 - 1/p))
        ratios.append(ratio)
    metric_value = sum(ratios) / len(ratios)
    conjecture_holds = all(r >= 0.75 for r in ratios)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Schatten p-Norm Ratio",
        "metric_value": metric_value,
        "instances_tested": len(ratios),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")