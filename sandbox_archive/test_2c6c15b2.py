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

def generate_3cnf(n: int, m: int) -> list:
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            sign = random.choice([-1, 1])
            if (var, sign) not in clause and (-var, -sign) not in clause:
                clause.add((var, sign))
        clauses.append(list(clause))
    return clauses

def fast_walsh_hadamard_transform(f: list) -> list:
    n = len(f)
    while n > 1:
        half = n // 2
        for i in range(half):
            for j in range(i, n, n):
                u = f[j]
                v = f[j + half]
                f[j] = u + v
                f[j + half] = (u - v) * math.sqrt(2)
        n //= 2
    return f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = 15 * n
    threshold = 2**(n/2) / (2**(n/2) // 10)
    
    f = [0] * (1 << n)
    for _ in range(m):
        clause = generate_3cnf(n, 1)[0]
        for var, sign in clause:
            f[1 << (var - 1)] += sign
    
    abs_sum = sum(abs(x) for x in f)
    
    conjecture_holds = abs_sum < threshold
    counterexample = "" if conjecture_holds else "threshold exceeded"
    
    return {
        "metric_name": "sum_of_abs_fourier_coeffs",
        "metric_value": abs_sum,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"threshold exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")