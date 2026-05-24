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
            return 'A'
        else:
            left = generate_and_or_tree(random.randint(1, n-1))
            right = generate_and_or_tree(n - len(left) - 1)
            return f'({left} OR {right})'
    
    def compute_coxeter_number(tree):
        if tree == 'A':
            return 2
        elif tree.startswith('('):
            left, _, right = tree[1:-1].partition(' OR ')
            return max(compute_coxeter_number(left), compute_coxeter_number(right))
        else:
            return float('inf')
    
    def depth(tree):
        if tree == 'A':
            return 1
        elif tree.startswith('('):
            left, _, right = tree[1:-1].partition(' OR ')
            return max(depth(left), depth(right)) + 1
        else:
            return float('inf')
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_depth = 0
        total_coxeter_number = 0
        
        while len(results) < 30:
            tree = generate_and_or_tree(n)
            coxeter_number = compute_coxeter_number(tree)
            tree_depth = depth(tree)
            
            if coxeter_number != float('inf') and tree_depth != float('inf'):
                instances_tested += 1
                total_depth += tree_depth
                total_coxeter_number += coxeter_number
                
                results.append({
                    "metric_name": "Coxeter Number vs Depth",
                    "metric_value": (total_depth / instances_tested, total_coxeter_number / instances_tested),
                    "instances_tested": instances_tested,
                    "conjecture_holds": abs((total_depth / instances_tested) - math.log(n)) <= 0.5 * math.log(n),
                    "counterexample": ""
                })
    
    if len(results) < 30:
        return {
            "metric_name": "Coxeter Number vs Depth",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_depth = sum(result["metric_value"][0] for result in results) / len(results)
    mean_coxeter_number = sum(result["metric_value"][1] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "Coxeter Number vs Depth",
        "metric_value": (mean_depth, mean_coxeter_number),
        "instances_tested": 30,
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(result["metric_value"][0] for result in results) / len(results)
    mean_coxeter_number = sum(result["metric_value"][1] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean_depth={mean_depth} mean_coxeter_number={mean_coxeter_number} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"depth_exceeds_log_n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")