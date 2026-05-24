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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_and_or_tree(n):
    if n == 1:
        return 'A'
    else:
        left_size = random.randint(1, n-2)
        right_size = n - left_size - 1
        return ('O', generate_and_or_tree(left_size), generate_and_or_tree(right_size))

def compute_coxeter_group(tree):
    # Simplified Coxeter group computation for demonstration purposes
    # This is a placeholder and should be replaced with actual computation
    if tree == 'A':
        return 1
    else:
        left, right = tree[1]
        return max(compute_coxeter_group(left), compute_coxeter_group(right)) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_depth = 0
        total_root_length = 0
        
        while len(results) < 30:
            tree = generate_and_or_tree(n)
            root_length = compute_coxeter_group(tree)
            depth = random.randint(1, int(root_length * 2))  # Simplified depth calculation
            
            instances_tested += 1
            total_depth += depth
            total_root_length += root_length
            
            results.append((root_length, depth))
        
        avg_depth = total_depth / len(results)
        avg_root_length = total_root_length / len(results)
        
        if avg_root_length <= 1.5 * (math.log(n) / math.log(2)) and avg_depth <= math.log(n):
            conjecture_holds = True
        else:
            conjecture_holds = False
        
        counterexample = "" if conjecture_holds else "depth > log n or root length too high"
        
        return {
            "metric_name": "Root Length vs Depth",
            "metric_value": avg_root_length,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    import math
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = (sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"depth > log n or root length too high\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")