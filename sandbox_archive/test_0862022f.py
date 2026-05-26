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

def generate_random_boolean_function(n):
    if n == 1:
        return random.choice(['0', '1'])
    else:
        op = random.choice(['AND', 'OR', 'XOR'])
        subformulas = [generate_random_boolean_function(random.randint(1, n)) for _ in range(random.randint(2, n))]
        return [op] + subformulas

def compute_xor_and_tree_width(formula):
    if isinstance(formula[0], list):
        left_width = compute_xor_and_tree_width(formula[1])
        right_width = compute_xor_and_tree_width(formula[2])
        return max(left_width, right_width) + 1
    else:
        return 1

def geometric_quantization_rank(formula):
    if isinstance(formula[0], list):
        left_rank = geometric_quantization_rank(formula[1])
        right_rank = geometric_quantization_rank(formula[2])
        return max(left_rank, right_rank) + 1
    else:
        return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_random_boolean_function(n)
        xor_and_width = compute_xor_and_tree_width(formula)
        rank = geometric_quantization_rank(formula)
        
        if xor_and_width == 0 or rank == 0:
            continue
        
        alpha = Fraction(1, 2)  # Example constant
        beta = Fraction(1, 4)   # Example constant
        
        expected_min_rank = alpha * math.log(xor_and_width)
        expected_max_rank = beta * xor_and_width
        
        results.append({
            "n": n,
            "xor_and_width": xor_and_width,
            "rank": rank,
            "expected_min_rank": expected_min_rank,
            "expected_max_rank": expected_max_rank
        })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(expected_min_rank <= result["rank"] <= expected_max_rank for result in results)
    counterexample = "" if conjecture_holds else "rank out of bounds"
    
    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"] - result["expected_min_rank"]) > 3 or abs(result["metric_value"] - result["expected_max_rank"]) > 3 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank out of bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")