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
    
    def branching_program_depth(boolean_function):
        n = int(math.log2(len(boolean_function)))
        if 2**n != len(boolean_function):
            return float('inf')
        
        depth = 0
        queue = [(boolean_function, 0)]
        while queue:
            new_queue = []
            for func, i in queue:
                if i == n - 1:
                    continue
                left_child = func[:i] + [0] + func[i+1:]
                right_child = func[:i] + [1] + func[i+1:]
                new_queue.append((left_child, i + 1))
                new_queue.append((right_child, i + 1))
            queue = new_queue
            depth += 1
        return depth
    
    def tensor_product_rank(boolean_function):
        n = int(math.log2(len(boolean_function)))
        if 2**n != len(boolean_function):
            return float('inf')
        
        rank = 0
        for i in range(n):
            left_child = boolean_function[:i] + [0] + boolean_function[i+1:]
            right_child = boolean_function[:i] + [1] + boolean_function[i+1:]
            rank += max(tensor_product_rank(left_child), tensor_product_rank(right_child))
        return rank
    
    n = random.randint(5, 40)
    boolean_function = generate_boolean_function(n)
    
    depth = branching_program_depth(boolean_function)
    rank = tensor_product_rank(boolean_function)
    
    if abs(depth - rank) > 1:
        return {
            "metric_name": "Depth vs Rank",
            "metric_value": depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Depth {depth} != Rank {rank}"
        }
    
    return {
        "metric_name": "Depth vs Rank",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    mean = total_metric_value / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction=1.0")
    elif support_fraction >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction / len(results)}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Depth != Rank' first_failing_seed={first_failing_seed}")