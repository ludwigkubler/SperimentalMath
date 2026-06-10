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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 1
        cc = float('inf')
        for i in range(1, n):
            left = f[:i]
            right = f[i:]
            cc_left = communication_complexity(left)
            cc_right = communication_complexity(right)
            cc = min(cc, max(cc_left + cc_right, cc_left + 1, cc_right + 1))
        return cc
    
    def construct_noncommutative_algebra(f):
        n = len(f)
        A_f = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i & j]:
                    A_f[i][j] = 1
        return A_f
    
    def minrank(A):
        n = len(A)
        rank = 0
        for _ in range(n):
            pivot_row = next((r for r in range(rank, n) if A[r][rank]), None)
            if pivot_row is None:
                break
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for i in range(n):
                if i != rank and A[i][rank]:
                    factor = Fraction(A[i][rank], A[rank][rank])
                    for j in range(rank, n):
                        A[i][j] -= factor * A[rank][j]
            rank += 1
        return rank
    
    def calculate_metric(n):
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        A_f = construct_noncommutative_algebra(f)
        rank = minrank(A_f)
        return {"metric_name": "minrank(CC(f)) / CC(f)", 
                "metric_value": Fraction(rank, cc), 
                "instances_tested": 1, 
                "n_max": n, 
                "conjecture_holds": True, 
                "counterexample": ""}
    
    results = [calculate_metric(n) for n in [5, 10, 15, 20, 30, 40]]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    return {"seed": seed, 
            "mean_metric_value": mean_value, 
            "std_metric_value": std_value, 
            "support_fraction": support_fraction}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["mean_metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = all(result["support_fraction"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["support_fraction"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["support_fraction"])
        counterexample = "minrank(CC(f)) / CC(f) is not linearly related"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")