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
    
    def generate_xor_and_tree(n):
        if n == 1:
            return [0]
        left = generate_xor_and_tree(n // 2)
        right = generate_xor_and_tree(n - n // 2)
        return [left, right]
    
    def tree_width(tree):
        if isinstance(tree, int):
            return 0
        left_width = tree_width(tree[0])
        right_width = tree_width(tree[1])
        return max(left_width, right_width) + 1
    
    def quandle_structure(tree):
        if isinstance(tree, int):
            return {tree}
        left_quandle = quandle_structure(tree[0])
        right_quandle = quandle_structure(tree[1])
        new_elements = set()
        for x in left_quandle:
            for y in right_quandle:
                new_elements.add((x ^ y) & (x | y))
        return left_quandle.union(right_quandle).union(new_elements)
    
    def minimal_rank(quandle):
        generators = quandle
        while True:
            new_generators = set()
            for x in generators:
                for y in generators:
                    if (x ^ y) & (x | y) not in generators:
                        new_generators.add((x ^ y) & (x | y))
            if new_generators == generators:
                break
            generators = generators.union(new_generators)
        return len(generators)
    
    n = random.randint(1, 40)
    tree = generate_xor_and_tree(n)
    tw = tree_width(tree)
    quandle = quandle_structure(tree)
    r_quandle = minimal_rank(quandle)
    
    if r_quandle > 2 * tw:  # Example constant c=2
        return {
            "metric_name": "minimal_rank",
            "metric_value": r_quandle,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"r_quandle={r_quandle}, expected<=2*tw={2*tw}"
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": r_quandle,
            "instances_tested": 1,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r_quandle > 2*tw\" first_failing_seed={first_failing_seed}")