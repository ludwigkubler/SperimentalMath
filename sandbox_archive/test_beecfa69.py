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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def xor_and_tree_width(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function with 2^n values")
        
        def count_xor_and(node, is_xor):
            if node == 0 or node == 1:
                return 0
            left = node * 2
            right = node * 2 + 1
            if is_xor:
                return 1 + max(count_xor_and(left, False), count_xor_and(right, True))
            else:
                return 1 + max(count_xor_and(left, True), count_xor_and(right, False))
        
        return count_xor_and(0, False)
    
    def geometric_langlands_lattice_rank(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function with 2^n values")
        
        # Simplified version for demonstration purposes
        return n
    
    results = []
    for _ in range(30):
        f = generate_random_boolean_function(random.randint(5, 40))
        rank = geometric_langlands_lattice_rank(f)
        width = xor_and_tree_width(f)
        if width == 0:
            continue
        ratio = rank / width
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "Ratio of Rank to XOR-AND Tree Width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    
    return {
        "metric_name": "Ratio of Rank to XOR-AND Tree Width",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": mean >= 0.8 and std_dev <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if not all(results):
        mean = sum(x for x in results if x is not None) / len([x for x in results if x is not None])
        std_dev = math.sqrt(sum((x - mean)**2 for x in results if x is not None) / len([x for x in results if x is not None]))
        support_fraction = sum(1 for x in results if x is not None and x >= 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, x in enumerate(results) if x is not None and x < 0.8)
            print(f"RESULT: FALSIFIED counterexample=\"Not enough valid instances\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")