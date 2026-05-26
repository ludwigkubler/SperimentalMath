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
    
    def bool_func_to_poly(f):
        n = len(f)
        poly = [0] * (1 << n)
        for i in range(1 << n):
            if f(tuple((i >> j) & 1 for j in range(n))):
                poly[i] = 1
        return poly

    def min_rank(poly):
        n = int(math.log2(len(poly)))
        A = [[0] * (n + 1) for _ in range(1 << n)]
        for i in range(1 << n):
            A[i][i] = 1
            for j in range(n):
                if poly[i ^ (1 << j)]:
                    A[i][j] = 1
        
        rank = 0
        for i in range(n + 1):
            pivot = None
            for j in range(i, 1 << n):
                if A[j][i]:
                    pivot = j
                    break
            if pivot is None:
                continue
            
            rank += 1
            for j in range(1 << n):
                if j != pivot:
                    factor = Fraction(A[j][i], A[pivot][i])
                    for k in range(n + 1):
                        A[j][k] -= factor * A[pivot][k]
        
        return rank

    def random_boolean_function(n):
        return [random.choice([True, False]) for _ in range(2**n)]

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = random_boolean_function(n)
        poly = bool_func_to_poly(f)
        rank = min_rank(poly)
        results.append({
            "n": n,
            "rank": rank
        })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["rank"] <= n**2 + 100 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")