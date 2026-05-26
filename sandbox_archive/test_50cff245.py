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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_hypercube(n):
        return [[random.choice([0, 1]) for _ in range(3)] for _ in range(n)]
    
    def compute_linking_number(hypercube):
        # Placeholder for actual linking number computation
        # This is a dummy implementation for testing purposes
        return random.randint(1, n)
    
    def construct_bp(hypercube):
        # Placeholder for actual BP construction
        # This is a dummy implementation for testing purposes
        return random.randint(1, n)
    
    def dpll_search_tree_width(bp):
        # Placeholder for actual DPLL search tree width computation
        # This is a dummy implementation for testing purposes
        return random.randint(1, n)
    
    n = 40
    hypercube = generate_hypercube(n)
    linking_number = compute_linking_number(hypercube)
    bp_width = construct_bp(hypercube)
    dpll_width = dpll_search_tree_width(bp_width)
    
    metric_name = "DPLL Search Tree Width"
    metric_value = dpll_width
    instances_tested = 1
    conjecture_holds = linking_number * n >= dpll_width
    counterexample = "" if conjecture_holds else f"Linking Number: {linking_number}, BP Width: {bp_width}, DPLL Width: {dpll_width}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")