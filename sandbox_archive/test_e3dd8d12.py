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
    
    def generate_quasigroup(n):
        q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                q[i][j] = (i + j) % n
        return q
    
    def min_index(q):
        n = len(q)
        count = 0
        for i in range(n):
            for j in range(n):
                if q[i][j] != (i + j) % n:
                    count += 1
        return count / (n * n)
    
    def matrix_from_quasigroup(q):
        n = len(q)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[q[i][j]][j] = 1
        return A
    
    def spectral_norm(A):
        n = len(A)
        v = [1.0 / math.sqrt(n)] * n
        for _ in range(100):  # Power iteration method
            v = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            norm = sum(x ** 2 for x in v)
            v = [x / math.sqrt(norm) for x in v]
        return max(abs(x) for x in v)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        q = generate_quasigroup(n)
        min_idx = min_index(q)
        A = matrix_from_quasigroup(q)
        rank = spectral_norm(A)
        results.append((min_idx, rank))
    
    correlation = sum((x - y) ** 2 for x, y in results) / len(results)
    mean_metric_value = correlation
    instances_tested = len(n_values)
    n_max = max(n_values)
    conjecture_holds = mean_metric_value >= 0.8 and mean_metric_value <= 3
    counterexample = "" if conjecture_holds else "correlation below threshold"
    
    return {
        "metric_name": "correlation",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = min(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation below threshold\" first_failing_seed={first_failing_seed}")