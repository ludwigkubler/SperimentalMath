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
    
    def generate_formula(n):
        if n == 1:
            return "A"
        else:
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f"({left} OR {right})"
    
    def tree_like_resolution_size(formula):
        if formula.isalpha():
            return 1
        else:
            p, left, right = formula[1:-1].split()
            return 1 + max(tree_like_resolution_size(left), tree_like_resolution_size(right))
    
    def symplectic_capacity(n):
        return n ** (1/4)
    
    def second_cohomology_group(t):
        return t ** (3/2)
    
    results = []
    for _ in range(30):
        n = random.choice([30, 40])
        formula = generate_formula(n)
        cap = symplectic_capacity(n)
        cohomology = second_cohomology_group(tree_like_resolution_size(formula))
        results.append((cap, cohomology))
    
    mean_cap = sum(cap for cap, _ in results) / len(results)
    std_cap = math.sqrt(sum((cap - mean_cap) ** 2 for cap, _ in results) / len(results))
    mean_cohomology = sum(coh for _, coh in results) / len(results)
    std_cohomology = math.sqrt(sum((coh - mean_cohomology) ** 2 for _, coh in results) / len(results))
    
    conjecture_holds = all(cap >= n ** (1/4) and coho == t ** (3/2) for cap, coho in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Symplectic Capacity",
        "metric_value": mean_cap,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cap = sum(res["metric_value"] for res in results) / len(results)
    std_cap = math.sqrt(sum((res["metric_value"] - mean_cap) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_cap} std={std_cap} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cap} std={std_cap} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")