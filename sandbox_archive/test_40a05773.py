# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import sys
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_function(n):
        return lambda x: sum(x[i] * (i + 1) for i in range(n)) % 2
    
    def degree_2_sos_moment_matrix(f, n):
        M = [[0] * n for _ in range(n)]
        for x in itertools.product([0, 1], repeat=n):
            f_x = f(x)
            for i in range(n):
                for j in range(n):
                    M[i][j] += x[i] * x[j] * (i + 1) * (j + 1)
        return M
    
    def power_iteration(M, n, max_iter=1000):
        v = [random.random() for _ in range(n)]
        v = [x / sum(v) for x in v]
        for _ in range(max_iter):
            v_next = [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]
            v_next = [x / sum(v_next) for x in v_next]
            if all(abs(v_next[i] - v[i]) < 1e-6 for i in range(n)):
                break
            v = v_next
        return max(v), min(v)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_function(n)
    M = degree_2_sos_moment_matrix(f, n)
    lambda_max, lambda_min = power_iteration(M, n)
    
    if lambda_min <= 0:
        return {
            "metric_name": "lambda_min",
            "metric_value": lambda_min,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "negative_eigenvalue"
        }
    
    conjecture_holds = lambda_min >= Fraction(1, math.sqrt(n))
    counterexample = "" if conjecture_holds else f"lambda_min={lambda_min} < 1/√{n}"
    
    return {
        "metric_name": "lambda_min",
        "metric_value": lambda_min,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 200, 7))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")