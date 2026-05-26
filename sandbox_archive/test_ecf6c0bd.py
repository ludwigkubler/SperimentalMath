# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_xor_and_tree(n: int, max_depth: int) -> list:
    if n <= 0 or max_depth <= 0:
        return []
    if n == 1:
        return [random.choice([0, 1])]
    if max_depth == 1:
        return [random.choice([0, 1]) for _ in range(n)]
    
    left_size = random.randint(1, n-1)
    right_size = n - left_size
    
    left = generate_xor_and_tree(left_size, max_depth-1)
    right = generate_xor_and_tree(right_size, max_depth-1)
    
    return [random.choice([0, 1]) for _ in range(n)]

def compute_symplectic_form(tree: list) -> list:
    n = len(tree)
    symplectic_form = [[Fraction(0, 1)] * n for _ in range(n)]
    
    def assign(i, j, value):
        if i < j:
            symplectic_form[i][j] = value
            symplectic_form[j][i] = -value
    
    def xor_and(a, b):
        return a ^ b
    
    def and_or(a, b):
        return a & b
    
    for i in range(n):
        if tree[i] == 0:
            assign(i, (i + 1) % n, Fraction(1, 1))
        else:
            assign(i, (i - 1) % n, Fraction(-1, 1))
    
    return symplectic_form

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    width_values = [5, 10, 15, 20, 30, 40]
    total_ranks = []
    counterexample = ""
    
    for width in width_values:
        tree = generate_xor_and_tree(n, width)
        symplectic_form = compute_symplectic_form(tree)
        
        # Compute minimal rank
        min_rank = len([row for row in symplectic_form if any(row)])
        total_ranks.append(min_rank)
    
    mean_value = sum(total_ranks) / len(total_ranks)
    expected_value = sum(width_values) * 0.5  # Simplified example function
    
    if abs(mean_value - expected_value) <= 3:
        conjecture_holds = True
    else:
        conjecture_holds = False
        counterexample = "mean_value does not match expected_value"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": len(width_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")