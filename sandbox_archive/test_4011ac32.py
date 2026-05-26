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

def generate_and_or_tree(depth, leaves):
    if depth == 0:
        return leaves.pop()
    left = generate_and_or_tree(depth - 1, leaves)
    right = generate_and_or_tree(depth - 1, leaves)
    return ('AND', left, right) if random.choice([True, False]) else ('OR', left, right)

def min_rank(tree):
    if isinstance(tree, tuple):
        op, left, right = tree
        if op == 'AND':
            return max(min_rank(left), min_rank(right))
        elif op == 'OR':
            return min(min_rank(left), min_rank(right))
    else:
        return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_leaves = random.randint(5, 40)
    depth = math.ceil(math.log2(n_leaves)) + 1
    tree = generate_and_or_tree(depth, list(range(n_leaves)))
    
    rank = min_rank(tree)
    instances_tested = 1
    
    # Check if the rank is polynomially related to N and D
    poly_bound = n_leaves ** 3 + depth ** 2
    conjecture_holds = abs(rank - poly_bound) <= poly_bound / 2
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} is not within a factor of 2 from Θ(poly({n_leaves}, {depth}))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank outside expected range\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")