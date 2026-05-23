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
    
    def generate_boolean_algebra(n):
        # Generate a random Boolean algebra with n generators
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalize(boolean_algebra):
        # Tropicalization of the Boolean algebra
        n = int(math.log2(len(boolean_algebra)))
        tropicalized = []
        for i in range(n):
            tropicalized.extend([min(a + b, a - b) for a, b in zip(boolean_algebra[:2**i], boolean_algebra[2**i:2**(i+1)])])
        return tropicalized
    
    def branching_program_depth(boolean_function):
        # Construct a branching program and determine its depth
        n = len(boolean_function)
        if n == 1:
            return 1
        mid = n // 2
        left_depth = branching_program_depth(boolean_function[:mid])
        right_depth = branching_program_depth(boolean_function[mid:])
        return max(left_depth, right_depth) + 1
    
    def tensor_product_rank(tropicalized):
        # Compute the tensor product rank of the tropicalized Boolean algebra
        n = int(math.log2(len(tropicalized)))
        rank = 0
        for i in range(n):
            rank += sum(1 for a, b in zip(tropicalized[:2**i], tropicalized[2**i:2**(i+1)]) if a != b)
        return rank
    
    n = random.randint(5, 40)  # Sweep n through at least 4 distinct sizes
    boolean_algebra = generate_boolean_algebra(n)
    tropicalized = tropicalize(boolean_algebra)
    depth = branching_program_depth(boolean_function=boolean_algebra)
    rank = tensor_product_rank(tropicalized)
    
    return {
        "metric_name": "depth_vs_rank",
        "metric_value": abs(depth - rank),
        "instances_tested": 1,
        "conjecture_holds": abs(depth - rank) <= 1,
        "counterexample": "" if abs(depth - rank) <= 1 else f"Depth {depth}, Rank {rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] > 1 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] > 1)
        print(f"RESULT: FALSIFIED counterexample='depth_greater_than_rank' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")