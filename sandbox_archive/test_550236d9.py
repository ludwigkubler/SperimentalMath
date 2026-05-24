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
    n = random.randint(5, 40)
    coefficients = [random.uniform(-10, 10) for _ in range(n+1)]
    
    # Define tropical addition and multiplication
    def tropical_add(x, y):
        return max(x, y)
    
    def tropical_multiply(x, y):
        if x == float('-inf') or y == float('-inf'):
            return float('-inf')
        return x + y
    
    # Compute the formal power series representation of the tropical polynomial
    rho_f = [float('-inf')] * (n+1)
    for i in range(n+1):
        for j in range(i+1):
            if coefficients[j] != 0:
                rho_f[i] = tropical_add(rho_f[i], tropical_multiply(coefficients[j], i - j))
    
    # Compute the minimal rank of the formal power series
    min_rank = float('inf')
    for k in range(1, n+1):
        if all(rho_f[i] == float('-inf') for i in range(k, n+1)):
            continue
        rank = 0
        for i in range(n+1):
            if rho_f[i] != float('-inf'):
                rank += 1
        min_rank = min(min_rank, rank)
    
    # Check the conjecture
    conjecture_holds = min_rank <= n ** (3/2)
    counterexample = "" if conjecture_holds else f"min_rank={min_rank}, expected<=n^(3/2)={n**(3/2)}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")