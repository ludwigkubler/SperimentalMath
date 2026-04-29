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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def free_entropy(matrix):
        # Approximate free entropy using a numerical method (simplified for demonstration)
        n = len(matrix)
        trace = sum(matrix[i][i] for i in range(n))
        det = 1
        for row in matrix:
            det *= abs(row[0])
        return trace - math.log(det)
    
    def disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                M[i][j] = random.choice([0, 1])
                M[j][i] = 1 - M[i][j]
        return M
    
    def communication_complexity(matrix):
        # Simplified approximation of communication complexity
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = disjointness_matrix(n)
        fe = free_entropy(M)
        cc = communication_complexity(M)
        results.append({"n": n, "fe": fe, "cc": cc})
    
    avg_fe = sum(result["fe"] for result in results) / len(results)
    avg_cc = sum(result["cc"] for result in results) / len(results)
    
    conjecture_holds = all(abs(result["fe"] - result["n"]) < 1e-2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "free_entropy",
        "metric_value": avg_fe,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(30)
        seeds = [p for p in primes]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_fe = sum(res["metric_value"] for res in results) / len(results)
    std_fe = math.sqrt(sum((res["metric_value"] - mean_fe) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_fe} std={std_fe} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")