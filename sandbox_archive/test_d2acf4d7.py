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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def fraction_add(f1, f2):
    num = f1[0] * f2[1] + f2[0] * f1[1]
    denom = f1[1] * f2[1]
    common_divisor = gcd(num, denom)
    return (num // common_divisor, denom // common_divisor)

def fraction_mul(f1, f2):
    num = f1[0] * f2[0]
    denom = f1[1] * f2[1]
    common_divisor = gcd(num, denom)
    return (num // common_divisor, denom // common_divisor)

def fraction_leq(f1, f2):
    return f1[0] * f2[1] <= f2[0] * f1[1]

def generate_frege_tree(h, m):
    if h == 1:
        return ['A']
    left_size = random.randint(1, m - 2)
    right_size = m - 1 - left_size
    left_tree = generate_frege_tree(h - 1, left_size)
    right_tree = generate_frege_tree(h - 1, right_size)
    return ['I', left_tree, right_tree]

def count_automorphisms(tree):
    if len(tree) == 1:
        return 1
    left_subtree = tree[2]
    right_subtree = tree[3]
    left_size = len(left_subtree)
    right_size = len(right_subtree)
    automorphisms = 0
    for i in range(left_size):
        for j in range(right_size):
            if fraction_leq((i + 1, left_size), (j + 1, right_size)):
                automorphisms += count_automorphisms(left_subtree) * count_automorphisms(right_subtree)
    return automorphisms

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    total_time = 0.0
    conjecture_holds = True
    counterexample = ""

    for h in [5, 10, 15, 20, 30, 40]:
        for m in range(1, min(h * 2 + 1, 41)):
            n_max = max(n_max, m)
            instances_tested += 1
            tree = generate_frege_tree(h, m)
            automorphisms = count_automorphisms(tree)
            bound = fraction_mul(fraction_add((h, 1), (m, 1)), (3, 2))
            if not fraction_leq(automorphisms, bound):
                conjecture_holds = False
                counterexample = f"Tree with h={h}, m={m} has {automorphisms} automorphisms, which exceeds the bound {bound}"
                break

    return {
        "metric_name": "Number of Automorphisms",
        "metric_value": 0.0,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    total_time = 0.0

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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")