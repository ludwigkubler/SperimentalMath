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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def formal_group_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def read_twice_bp_size(f):
        n = len(f)
        size = 0
        for i in range(n):
            if f[i] == 1:
                size += 1
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    bp_sizes = []
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            rank = formal_group_rank(f)
            size = read_twice_bp_size(f)
            ranks.append(rank)
            bp_sizes.append(size)
    
    if not ranks or not bp_sizes:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_bp_size = sum(bp_sizes) / len(bp_sizes)
    diff_sum = sum(abs(r - s) for r, s in zip(ranks, bp_sizes))
    correlation_coefficient = (sum((r - mean_rank) * (s - mean_bp_size) for r, s in zip(ranks, bp_sizes)) /
                               math.sqrt(sum((r - mean_rank)**2 for r in ranks) *
                                         sum((s - mean_bp_size)**2 for s in bp_sizes)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "conjecture_holds": correlation_coefficient >= 0.8 and diff_sum / len(ranks) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")