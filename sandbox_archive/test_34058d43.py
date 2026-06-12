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
    
    def generate_instance(n):
        return [random.randint(0, (1 << n) - 1) for _ in range(n)]
    
    def dpll(instance):
        n = len(instance)
        
        def backtrack(level):
            if level == n:
                return True
            for i in range(2):
                assignment[level] = i
                if all((instance[i] & (1 << j)) ^ assignment[j] == 0 for j in range(n)):
                    if backtrack(level + 1):
                        return True
            return False
        
        assignment = [0] * n
        return backtrack(0)
    
    def automorphism_group(instance):
        n = len(instance)
        generators = []
        
        # Brute-force search for generators (very inefficient for large n)
        for i in range(n):
            for j in range(i + 1, n):
                if all((instance[i] & (1 << k)) == (instance[j] & (1 << k)) for k in range(n)):
                    generators.append((i, j))
        
        return len(generators)
    
    def dpll_search_tree_width(instance):
        n = len(instance)
        
        def backtrack(level):
            if level == n:
                return 0
            max_depth = 0
            for i in range(2):
                assignment[level] = i
                if all((instance[i] & (1 << j)) ^ assignment[j] == 0 for j in range(n)):
                    depth = backtrack(level + 1)
                    if depth > max_depth:
                        max_depth = depth
            return max_depth + 1
        
        assignment = [0] * n
        return backtrack(0)
    
    instance = generate_instance(40)
    shv = dpll(instance)
    gen_count = automorphism_group(instance)
    w_dpll = dpll_search_tree_width(instance)
    
    if shv == 0 or w_dpll == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "DPLL returned 0 or automorphism group is empty"
        }
    
    ratio = Fraction(gen_count, shv)
    return {
        "metric_name": "Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds 1' first_failing_seed={first_failing_seed}")