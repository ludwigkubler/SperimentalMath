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

def primes_up_to(n):
    sieve = [True] * (n + 1)
    for x in range(2, int(math.sqrt(n)) + 1):
        if sieve[x]:
            for i in range(x*x, n + 1, x):
                sieve[i] = False
    return [x for x in range(2, n + 1) if sieve[x]]

def random_tree(width, height):
    if height == 0:
        return []
    children = [random_tree(random.randint(1, width), height - 1) for _ in range(random.randint(1, width))]
    return [(children[0], children[1])] + children[2:]

def deligne_lusztig_cone(tree):
    if not tree:
        return 0
    nodes = set()
    def traverse(node):
        if isinstance(node, tuple):
            nodes.add(node)
            traverse(node[0])
            traverse(node[1])
        else:
            for n in node:
                nodes.add(n)
    traverse(tree)
    rank = len(nodes)
    return rank

def min_rank(tree):
    rank = deligne_lusztig_cone(tree)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    widths = [5, 10, 15, 20, 30, 40]
    heights = [random.randint(1, 5) for _ in range(len(widths))]
    results = []
    for w, h in zip(widths, heights):
        tree = random_tree(w, h)
        rho = min_rank(tree)
        results.append(rho)
    mean_rho = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= (w**2 / h)) / len(results)
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else f"rho > O(w^2/h) for some seed"
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rho,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else primes_up_to(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result["metric_value"])
    
    mean_rho = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= (w**2 / h)) / len(results)
    if all(r <= (w**2 / h) for w, h, r in zip(widths, heights, results)):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not conjecture_holds)
        print(f"RESULT: FALSIFIED counterexample=\"rho > O(w^2/h)\" first_failing_seed={first_failing_seed}")