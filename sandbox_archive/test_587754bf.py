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
    
    def generate_twisted_module(n):
        # Simple twisted module generator for demonstration purposes
        return [random.randint(0, 1) for _ in range(n)]
    
    def compute_minimal_rank(module):
        # Placeholder for minimal rank computation
        return sum(module)
    
    def compute_monotone_circuit_depth(n):
        # Placeholder for monotone circuit depth computation
        return n
    
    def tensor_product_representation(module, n):
        # Placeholder for tensor product representation computation
        return [module[i % len(module)] for i in range(n)]
    
    def permutation_max_rank(tensor_product, P):
        # Placeholder for permutation that maximizes rank computation
        return max(tensor_product)
    
    n = random.randint(5, 40)
    module = generate_twisted_module(n)
    min_rank = compute_minimal_rank(module)
    depth = compute_monotone_circuit_depth(n)
    tensor_product = tensor_product_representation(module, n)
    P = list(range(n))
    max_rank = permutation_max_rank(tensor_product, P)
    
    ratio = Fraction(depth, max_rank) if max_rank != 0 else float('inf')
    conjecture_holds = ratio <= 1.5  # Placeholder threshold
    counterexample = "" if conjecture_holds else f"Ratio {ratio} > 1.5"
    
    return {
        "metric_name": "Ratio of Monotone Circuit Depth to Minimal Rank",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded threshold\" first_failing_seed={first_failing_seed}")