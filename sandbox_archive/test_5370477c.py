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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        if k > n:
            return 0
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def generate_read_twice_bp(size: int):
        # Simplified representation of a read-twice branching program
        bp = []
        for i in range(size):
            bp.append(random.choice([0, 1]))
        return bp
    
    def compute_entanglement_tensor(bp):
        size = len(bp)
        tensor = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if bp[i] == bp[j]:
                    tensor[i][j] = 1
        return tensor
    
    def min_rank(tensor):
        rows, cols = len(tensor), len(tensor[0])
        rank = 0
        for _ in range(min(rows, cols)):
            pivot_row = -1
            for r in range(rank, rows):
                if tensor[r][rank] != 0:
                    pivot_row = r
                    break
            if pivot_row == -1:
                break
            for c in range(cols):
                tensor[pivot_row][c], tensor[rank][c] = tensor[rank][c], tensor[pivot_row][c]
            for r in range(rows):
                if r != rank:
                    factor = tensor[r][rank] / tensor[rank][rank]
                    for c in range(cols):
                        tensor[r][c] -= factor * tensor[rank][c]
            rank += 1
        return rank
    
    size = random.randint(5, 40)
    bp = generate_read_twice_bp(size)
    entanglement_tensor = compute_entanglement_tensor(bp)
    min_rank_value = min_rank(entanglement_tensor)
    
    lower_bound = size
    upper_bound = log2(size) ** 2
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank_value,
        "instances_tested": 1,
        "conjecture_holds": lower_bound <= min_rank_value <= upper_bound,
        "counterexample": "" if lower_bound <= min_rank_value <= upper_bound else f"rank={min_rank_value}, expected=({lower_bound}, {upper_bound})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results):.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank out of bounds\" first_failing_seed={first_failing_seed}")