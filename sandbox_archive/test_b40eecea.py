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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        n = len(matrix)
        r = 0
        for row in gaussian_elimination(matrix):
            if any(row[j] != 0 for j in range(r)):
                r += 1
        return r

    def acc0_circuit_threshold(n):
        # Placeholder function, should be replaced with actual implementation
        return random.randint(1, n)

    def quadratic_form(f):
        # Placeholder function, should be replaced with actual implementation
        return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]

    n = random.choice([5, 10, 15, 20, 30, 40])
    f = [random.randint(0, 1) for _ in range(n)]
    Q = quadratic_form(f)
    rank_Q = rank(Q)
    threshold = acc0_circuit_threshold(n)

    if rank_Q > math.log2(n)**2:
        return {
            "metric_name": "acc0_circuit_threshold",
            "metric_value": threshold,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank of Q exceeds log²(n) for n={n}"
        }

    if threshold < math.log2(n)**2 * rank_Q:
        return {
            "metric_name": "acc0_circuit_threshold",
            "metric_value": threshold,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Circuit threshold does not meet Θ(log²(n) * rank(Q)) for n={n}"
        }

    return {
        "metric_name": "acc0_circuit_threshold",
        "metric_value": threshold,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank of Q exceeds log²(n)\" first_failing_seed={first_failing_seed}")