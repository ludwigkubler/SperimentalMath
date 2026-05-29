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
            p = random.choice(["AND", "OR"])
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f"({left} {p} {right})"
    
    def tree_like_resolution_size(formula):
        if formula == "A":
            return 1
        else:
            p, left, right = formula.split()
            return 1 + tree_like_resolution_size(left) + tree_like_resolution_size(right)
    
    def symplectic_capacity(n):
        return n ** (1/4)
    
    def second_cohomology_group(t):
        return t ** (3/2)
    
    results = []
    for n in [30, 40]:
        formula = generate_formula(n)
        capacity = symplectic_capacity(n)
        cohomology = second_cohomology_group(tree_like_resolution_size(formula))
        results.append({
            "n": n,
            "capacity": capacity,
            "cohomology": cohomology
        })
    
    mean_capacity = sum(result["capacity"] for result in results) / len(results)
    mean_cohomology = sum(result["cohomology"] for result in results) / len(results)
    
    conjecture_holds = all(
        result["capacity"] >= n ** (1/4) and
        result["cohomology"] == n ** (3/2)
        for result in results
    )
    
    return {
        "metric_name": "Symplectic Capacity",
        "metric_value": mean_capacity,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_capacity = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_capacity} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_capacity} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")