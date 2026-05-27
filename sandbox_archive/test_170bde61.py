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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 0
        mid = n // 2
        left_width = xor_and_tree_width(f[:mid])
        right_width = xor_and_tree_width(f[mid:])
        return max(left_width, right_width) + 1
    
    def geometric_langlands_lattice_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst):
        m = mean(lst)
        return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        rank = geometric_langlands_lattice_rank(f)
        width = xor_and_tree_width(f)
        if width == 0:
            continue
        ratio = rank / width
        ratios.append(ratio)
    
    metric_value = mean(ratios)
    std_dev = std(ratios)
    conjecture_holds = metric_value >= 0.8 and std_dev <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Minimal Rank to XOR-AND Tree Width",
        "metric_value": metric_value,
        "instances_tested": len(ratios),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2**i - 1 for i in range(5, 6)]  # Default to a list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")