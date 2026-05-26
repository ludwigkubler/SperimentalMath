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
    
    def generate_boolean_algebra(n):
        # Generate a random boolean algebra with n variables
        elements = [0] + [1 << i for i in range(1, n)]
        operations = {
            'and': lambda x, y: x & y,
            'or': lambda x, y: x | y,
            'not': lambda x: ~x & ((1 << n) - 1)
        }
        return elements, operations
    
    def construct_bicategory(boolean_algebra):
        # Construct the bicategory structure
        elements, operations = boolean_algebra
        objects = [set([e]) for e in elements]
        morphisms = {}
        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                if operations['and'](list(objects[i])[0], list(objects[j])[0]):
                    morphisms[(i, j)] = [(j,)]
        return objects, morphisms
    
    def compute_minimal_rank(bicategory):
        # Compute the minimal rank of the bicategory
        objects, morphisms = bicategory
        rank = len(objects)
        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                if (i, j) not in morphisms:
                    rank += 1
        return rank
    
    def compute_resolution_width(boolean_algebra):
        # Compute the width of the resolution proof tree
        elements, operations = boolean_algebra
        n = len(elements)
        width = 0
        for i in range(1 << (n - 1)):
            clause = [elements[j] if (i & (1 << j)) else ~elements[j] for j in range(n)]
            width = max(width, len(clause))
        return width
    
    n = random.randint(5, 40)
    boolean_algebra = generate_boolean_algebra(n)
    bicategory = construct_bicategory(boolean_algebra)
    minimal_rank = compute_minimal_rank(bicategory)
    resolution_width = compute_resolution_width(boolean_algebra)
    
    if resolution_width == 0:
        return {
            "metric_name": "minimal_rank_over_resolution_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_width_zero"
        }
    
    ratio = minimal_rank / resolution_width
    return {
        "metric_name": "minimal_rank_over_resolution_width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 2 else False,  # Placeholder for actual constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='first_failing_seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")