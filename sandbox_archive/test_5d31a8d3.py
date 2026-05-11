# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def fast_walsh_hadamard_transform(f):
    n = len(f)
    if n == 1:
        return f
    even = fast_walsh_hadamard_transform(f[0::2])
    odd = fast_walsh_hadamard_transform(f[1::2])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def discrepancy(G, n):
    def sample_discrepancy():
        s = random.sample(range(1, n), n // 2)
        A = [0] * n
        for i in range(n):
            if i in s:
                A[i] = 1
            else:
                A[i] = -1
        return abs(sum(G[i][j] * (A[i] + A[j]) for i, j in combinations(range(n), 2)))
    return sum(sample_discrepancy() for _ in range(10)) / 10

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    f_hat = fast_walsh_hadamard_transform([sum(G[i][j] for j in range(n)) - n / 2 for i in range(n)])
    metric_value = sum(abs(x) for x in f_hat)
    delta = discrepancy(G, n)
    conjecture_holds = abs(metric_value * delta - 1) < 1e-6
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Fourier Coefficient Sum",
        "metric_value": metric_value,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")