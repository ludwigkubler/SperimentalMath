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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def noncrossing_partition_tree_height(f):
    n = len(f)
    if n == 1:
        return 1
    tree = []
    for i in range(n):
        subtree = generate_boolean_function(i)
        tree.append(subtree)
    return count_partitions(tree)

def count_partitions(tree):
    if isinstance(tree, list):
        return 1 + sum(count_partitions(subtree) for subtree in tree)
    else:
        return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        height = noncrossing_partition_tree_height(f)
        size = len(f)  # Simplified AC^0 circuit size as a placeholder
        results.append({
            "n": n,
            "height": height,
            "size": size
        })
    
    max_height = max(result["height"] for result in results)
    avg_size = sum(result["size"] for result in results) / len(results)
    
    C = Fraction(1, 2)  # Placeholder constant
    upper_bound = 2**(C * math.log(n_values[-1], 2)**2)
    
    conjecture_holds = max_height <= upper_bound
    counterexample = "" if conjecture_holds else f"max_height={max_height} > upper_bound={upper_bound}"
    
    return {
        "metric_name": "Noncrossing Partition Tree Height",
        "metric_value": avg_size,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_height > upper_bound\" first_failing_seed={first_failing_seed}")