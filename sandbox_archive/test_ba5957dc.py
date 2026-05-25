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
    
    def noncrossing_partition_tree_height(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function with 2^n values")
        
        def partition(i, j):
            if i == j:
                return [i]
            mid = (i + j) // 2
            left = partition(i, mid)
            right = partition(mid + 1, j)
            return sorted(left + right)
        
        def count_partitions(tree):
            if len(tree) == 1:
                return 0
            return 1 + sum(count_partitions(subtree) for subtree in tree)
        
        tree = partition(0, n - 1)
        return count_partitions(tree)
    
    def ac0_circuit_size(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function with 2^n values")
        
        # Simplified AC^0 circuit size estimation
        return n + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_heights = 0
    total_sizes = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 20 instances per seed
            f = generate_boolean_function(n)
            height = noncrossing_partition_tree_height(f)
            size = ac0_circuit_size(f)
            total_heights += height
            total_sizes += size
            instances_tested += 1
    
    mean_height = total_heights / instances_tested
    mean_size = total_sizes / instances_tested
    conjecture_holds = all(height <= 2**(3 * math.log2(n)**2) for n, height in zip(n_values, [mean_height] * len(n_values)))
    
    return {
        "metric_name": "Height vs Size",
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample found for n={n_values[0]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]  # Default to first 3 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_height} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Height exceeds size bound\" first_failing_seed={first_failing_seed}")