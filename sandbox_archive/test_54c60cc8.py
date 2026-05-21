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

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def frobenius_norm(A):
        norm = 0
        for row in A:
            for val in row:
                norm += abs(val) ** 2
        return math.sqrt(norm)

    def hypercontractive_constant(d, n):
        return (1 - 1 / d) ** (n // 2)

    def sos_approximation(tensor, d):
        # Placeholder function for SOS approximation algorithm
        # This is a dummy implementation and should be replaced with actual logic
        return random.random()

    def tensor_power(tensor, power):
        result = tensor[:]
        for _ in range(1, power):
            result = matrix_multiply(result, tensor)
        return result

    n = 20  # Size of the tensor
    d = 3   # Degree of the SOS approximation algorithm
    p = 100  # Number of trials per seed

    metric_values = []
    for _ in range(p):
        tensor = [[random.random() for _ in range(n)] for _ in range(n)]
        power = random.randint(5, 40)
        norm = frobenius_norm(tensor_power(tensor, power))
        hyper_const = hypercontractive_constant(d, n)
        if norm > hyper_const:
            metric_values.append(norm)

    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(x <= math.exp(-n / (2 * d)) for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Frobenius Norm Exceeding Hypercontractive Constant",
        "metric_value": mean_value,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")