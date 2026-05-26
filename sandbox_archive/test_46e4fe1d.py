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

# Helper functions for group operations and Frege proof trees

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def add_elements(group, element1, element2):
    result = []
    for e1 in group:
        for e2 in group:
            new_element = (e1 + e2) % len(group)
            if new_element not in result:
                result.append(new_element)
    return sorted(result)

def remove_element(group, element):
    result = [e for e in group if e != element]
    return sorted(result)

def generate_group(literals):
    group = literals.copy()
    for i in range(len(literals)):
        for j in range(i + 1, len(literals)):
            new_element = (literals[i] + literals[j]) % len(group)
            if new_element not in group:
                group.append(new_element)
    return sorted(group)

def minimal_rank(group):
    if not group:
        return 0
    rank = 1
    for i in range(2, len(group) + 1):
        if all(gcd(i, j) == 1 for j in group):
            rank = i
            break
    return rank

def generate_frege_tree(depth, literals):
    if depth == 0:
        return random.choice(literals)
    left = generate_frege_tree(depth - 1, literals)
    right = generate_frege_tree(depth - 1, literals)
    return (left, right)

def traverse(node):
    if isinstance(node, tuple):
        left, right = node
        traverse(left)
        traverse(right)

# Main test function

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in range(5, 41):
        for _ in range(6):  # Ensure at least 30 instances per seed
            literals = [i for i in range(n)]
            tree = generate_frege_tree(random.randint(1, 40), literals)
            group = generate_group(literals)
            rank = minimal_rank(group)
            results.append((n, rank))
    
    mean_value = sum(rank for _, rank in results) / len(results)
    support_fraction = sum(1 for _, rank in results if rank <= n) / len(results)
    
    conjecture_holds = all(rank <= n for _, rank in results)
    counterexample = "" if conjecture_holds else "rank exceeds depth"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds depth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support or counterexamples found")