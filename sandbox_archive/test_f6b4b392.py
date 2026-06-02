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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + random.randint(0, n - i - 1)
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        pivot = A[i][i]
        for j in range(i + 1, n):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    tsi_values = []
    r_values = []
    
    for n in n_values:
        d = random.randint(2, min(n - 1, 3))
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    G[i][j] = G[j][i] = 1
        A = []
        b = []
        for i in range(n):
            row = [0] * (n + 1)
            row[i] = 1
            for j in range(n):
                if G[i][j]:
                    row[j] += 1
            A.append(row)
            b.append(1 - d)
        
        try:
            x = gaussian_elimination(A, b)
            tsi = sum(abs(x[i]) for i in range(n))
            r = sum(abs(x[i]) for i in range(n)) / n
            tsi_values.append(tsi)
            r_values.append(r)
        except Exception as e:
            return {
                "metric_name": "tsi(G) - r(φ_G)",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    
    diff = [abs(tsi - r) for tsi, r in zip(tsi_values, r_values)]
    mean_diff = sum(diff) / len(diff)
    correlation_coefficient = sum((tsi - mean_tsi) * (r - mean_r) for tsi, r in zip(tsi_values, r_values)) / (len(diff) * math.sqrt(sum((tsi - mean_tsi) ** 2 for tsi in tsi_values)) * math.sqrt(sum((r - mean_r) ** 2 for r in r_values)))
    
    return {
        "metric_name": "tsi(G) - r(φ_G)",
        "metric_value": mean_diff,
        "instances_tested": len(diff),
        "n_max": max(n_values),
        "conjecture_holds": all(abs(d) <= 0.1 for d in diff) and correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_diff) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"]):
        print(f"RESULT: FALSIFIED counterexample=\"{results[results.index(next(filter(lambda r: r['conjecture_holds'] == False, results), None))]['counterexample']}\" first_failing_seed={seeds[results.index(next(filter(lambda r: r['conjecture_holds'] == False, results), None))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_evidence n_tested={len(results)}")