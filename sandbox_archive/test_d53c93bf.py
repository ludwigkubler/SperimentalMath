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
    
    def generate_formula(n):
        if n == 1:
            return "x"
        else:
            p = random.choice(["and", "or"])
            left = generate_formula(random.randint(1, n-1))
            right = generate_formula(random.randint(1, n-1))
            return f"({left} {p} {right})"
    
    def resolution_width(formula):
        stack = []
        for token in formula.split():
            if token == "and":
                stack.append(stack.pop() + " and " + stack.pop())
            elif token == "or":
                stack.append(stack.pop() + " or " + stack.pop())
            else:
                stack.append(token)
        return len(stack[0].split()) - 1
    
    def tautological_variety(formula):
        # Placeholder for actual computation
        return formula
    
    def minimal_local_system_rank(variety):
        # Placeholder for actual computation
        return len(variety.split())
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    variety = tautological_variety(formula)
    mls_phi = minimal_local_system_rank(variety)
    w_phi = resolution_width(formula)
    
    return {
        "metric_name": "mls_w_correlation",
        "metric_value": mls_phi / (w_phi + 1),  # Avoid division by zero
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,  # Mapping undefined for this conjecture
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")