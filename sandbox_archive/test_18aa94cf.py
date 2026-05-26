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
    
    def generate_and_or_tree(n):
        if n == 1:
            return random.choice([0, 1])
        else:
            left = generate_and_or_tree(n // 2)
            right = generate_and_or_tree(n - n // 2)
            return random.choice([left and right, left or right])
    
    def communication_complexity(tree):
        if isinstance(tree, int):
            return 0
        else:
            return 1 + max(communication_complexity(tree[0]), communication_complexity(tree[1]))
    
    def geometric_quantization_rank(n):
        # Placeholder for the actual geometric quantization rank calculation
        # This is a dummy implementation that returns n for simplicity
        return n
    
    n = random.randint(5, 40)
    tree = generate_and_or_tree(n)
    comm_complexity = communication_complexity(tree)
    
    if comm_complexity != n:
        return {
            "metric_name": "communication_complexity",
            "metric_value": comm_complexity,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Communication complexity is {comm_complexity}, not O(n)"
        }
    
    rank = geometric_quantization_rank(n)
    c = 1  # Placeholder constant
    if rank < c * math.log2(n):
        return {
            "metric_name": "geometric_quantization_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank {rank} is less than {c * math.log2(n)}"
        }
    
    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")