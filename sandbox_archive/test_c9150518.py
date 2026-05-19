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
    
    def generate_function(n):
        # Generate a random linear function over {0,1}^n
        coefficients = [random.randint(0, 1) for _ in range(n)]
        return lambda x: sum(c * xi for c, xi in zip(coefficients, x)) % 2

    def sos_moment_matrix(f, n):
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                x = [random.randint(0, 1) for _ in range(n)]
                A[i][j] += f(x) * f(x)
                A[j][i] += f(x) * f(x)
        return A

    def power_iteration(A, v, max_iter=100):
        for _ in range(max_iter):
            Av = [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(v))]
            v_norm = sum(x**2 for x in Av)**0.5
            v = [x / v_norm for x in Av]
        return max(abs(x) for x in Av)

    n = 10  # Start with a small size and increase if necessary
    f = generate_function(n)
    A = sos_moment_matrix(f, n)
    lambda_min = power_iteration(A, [random.random() for _ in range(n + 1)])

    metric_value = lambda_min / math.sqrt(n)
    conjecture_holds = metric_value >= Fraction(1, math.sqrt(n))
    counterexample = "" if conjecture_holds else "lambda_min < 1/sqrt(n)"

    return {
        "metric_name": "lambda_min",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"lambda_min < 1/sqrt(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")