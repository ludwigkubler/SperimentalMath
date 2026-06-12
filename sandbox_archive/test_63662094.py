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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def minimal_geometric_entropy(phi_G, n):
    if n == 0:
        return 0
    A = [[phi_G[i * (i + 1) // 2 + j] for j in range(i + 1)] for i in range(n)]
    try:
        det = determinant(gaussian_elimination(A))
    except IndexError:
        return float('inf')
    if det == 0:
        return float('inf')
    entropy = -math.log(abs(det)) / math.log(2)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    H_min_values = []
    w_values = []

    for n in n_values:
        phi_G = [random.choice([0, 1]) for _ in range(n * (n + 1) // 2)]
        H_min = minimal_geometric_entropy(phi_G, n)
        if H_min == float('inf'):
            continue
        w = random.randint(1, 100)  # Simulate resolution proof width
        H_min_values.append(H_min)
        w_values.append(w)

    if len(H_min_values) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": float('nan'),
            "instances_tested": len(H_min_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    mean_H_min = sum(H_min_values) / len(H_min_values)
    mean_w = sum(w_values) / len(w_values)

    correlation_coefficient = 0
    for H, w in zip(H_min_values, w_values):
        correlation_coefficient += (H - mean_H_min) * (w - mean_w)
    correlation_coefficient /= (len(H_min_values) * math.sqrt(sum((H - mean_H_min) ** 2 for H in H_min_values)) * math.sqrt(sum((w - mean_w) ** 2 for w in w_values)))

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(H_min_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    H_min_values = [r["metric_value"] for r in results if not math.isnan(r["metric_value"])]
    w_values = [r["instances_tested"] for r in results if not math.isnan(r["metric_value"])]

    mean_H_min = sum(H_min_values) / len(H_min_values)
    std_H_min = math.sqrt(sum((H - mean_H_min) ** 2 for H in H_min_values) / len(H_min_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_H_min:.6f} std={std_H_min:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first_failing_seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")