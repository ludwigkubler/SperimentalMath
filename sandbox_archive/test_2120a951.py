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
    
    def generate_random_function(n, depth):
        if depth == 1:
            return random.choice([0, 1])
        else:
            op = random.choice(['&', '|'])
            left = generate_random_function(n, depth - 1)
            right = generate_random_function(n, depth - 1)
            return (op, left, right)

    def evaluate_function(func, n):
        if isinstance(func, int):
            return func
        else:
            op, left, right = func
            if op == '&':
                return evaluate_function(left, n) & evaluate_function(right, n)
            elif op == '|':
                return evaluate_function(left, n) | evaluate_function(right, n)

    def tropicalize_function(func):
        if isinstance(func, int):
            return func
        else:
            op, left, right = func
            if op == '&':
                return max(tropicalize_function(left), tropicalize_function(right))
            elif op == '|':
                return min(tropicalize_function(left), tropicalize_function(right))

    def compute_rank(f, n):
        values = set()
        for i in range(2**n):
            inputs = [i >> j & 1 for j in range(n)]
            value = evaluate_function(f, n)
            values.add(value)
        return len(values)

    n = random.randint(5, 40)
    depth = random.randint(1, 3)
    f = generate_random_function(n, depth)
    
    rank = compute_rank(tropicalize_function(f), n)
    
    metric_name = "Minimal Rank of Tropicalized Quantum Groups"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= depth * math.log2(n)
    counterexample = "" if conjecture_holds else f"Function with rank {rank} and depth {depth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # First seed is 2 to avoid 1
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")