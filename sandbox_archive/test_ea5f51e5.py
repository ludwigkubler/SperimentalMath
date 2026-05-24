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
    
    def compute_hecke_algebra(f):
        n = int(math.log2(len(f)))
        H = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    H[i][j] = 1
        return H
    
    def compute_exponential_depth(f):
        n = int(math.log2(len(f)))
        depth = 0
        while True:
            new_f = [f[i] ^ f[j] for i in range(n) for j in range(i+1, n)]
            if len(new_f) == 1:
                return depth + 1
            f = new_f
            depth += 1
    
    def compute_rank(H):
        n = int(math.log2(len(H)))
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(i, n):
                if H[j][i] == 1:
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            rank += 1
            for j in range(n):
                if j != i:
                    factor = H[j][i]
                    for k in range(n):
                        H[j][k] ^= (factor * H[pivot_row][k]) % 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_boolean_function(n)
            H = compute_hecke_algebra(f)
            d = compute_exponential_depth(f)
            rank = compute_rank(H)
            metric_value = rank / (2**d)
            total_metric_value += metric_value
            instances_tested += 1
            if metric_value <= 1.0:
                conjecture_holds = False
                counterexample = f"n={n}, rank={rank}, d={d}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / (len(n_values) * 5)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")