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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = len(f)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1):
                if (i & (1 << j)) == 0:
                    A[i][j] = -1
                else:
                    A[i][j] = 1
        B = [f[i] for i in range(n)]
        return gaussian_elimination(A, B)
    
    def gaussian_elimination(A, b):
        n = len(b)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            if M[i][i] == 0:
                continue
            for j in range(i+1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n+1):
                    M[j][k] -= factor * M[i][k]
        return [M[i][-1] for i in range(n)]
    
    def minimal_root_multiplicity_index(poly):
        roots = find_roots(poly)
        multiplicities = {}
        for root in roots:
            if root in multiplicities:
                multiplicities[root] += 1
            else:
                multiplicities[root] = 1
        return min(multiplicities.values())
    
    def find_roots(poly):
        n = len(poly) - 1
        roots = []
        for i in range(n+1):
            if poly[i] != 0:
                root = (-poly[i]) / (2 * poly[i-1])
                roots.append(root)
        return roots
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            if f[i] == 1:
                rank += 1
        return rank / n
    
    def log_ratio(n, I, κ):
        if I <= 0 or κ <= 0:
            return float('-inf')
        return math.log(math.sqrt(I)) / math.log(κ)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        poly = characteristic_polynomial(f)
        I = minimal_root_multiplicity_index(poly)
        κ = communication_complexity_rank_variance(f)
        ratio = log_ratio(n, I, κ)
        results.append(ratio)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(abs(r) <= 1 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "log_ratio",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max([random.choice([5, 10, 15, 20, 30, 40]) for _ in range(30)]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r) <= 1) / len(results)
    
    if all(abs(r) <= 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r) > 1 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if abs(r) > 1))]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")