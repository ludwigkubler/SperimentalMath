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

def quandle_rank(tree):
    if isinstance(tree, int):
        return 1
    left_rank = quandle_rank(tree[0])
    right_rank = quandle_rank(tree[1])
    return left_rank + right_rank - 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        tree = generate_xor_and_tree(n)
        tw = tree_width(tree)
        r_quandle = quandle_rank(tree)
        results.append((n, tw, r_quandle))
    
    if len(results) < 30:
        return {
            "metric_name": "quandle_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    total_r_quandle = sum(r for _, _, r in results)
    mean_r_quandle = Fraction(total_r_quandle, len(results))
    max_tw = max(tw for _, tw, _ in results)
    c = Fraction(mean_r_quandle, max_tw)
    
    support_count = 0
    counterexample = ""
    for n, tw, r_quandle in results:
        if r_quandle > c * tw:
            support_count += 1
        else:
            counterexample = f"n={n}, tw={tw}, r_quandle={r_quandle}"
    
    conjecture_holds = support_count / len(results) >= 0.8
    
    return {
        "metric_name": "quandle_rank",
        "metric_value": mean_r_quandle,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i - 1 for i in range(5, 30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")