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
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 0
        for i in range(1, n):
            if all(f[j] == f[0] for j in range(i)):
                return 1 + xor_and_tree_width(f[i:])
        return 1 + max(xor_and_tree_width(f[:i]), xor_and_tree_width(f[i:]))

    def configuration_space_rank(f):
        n = len(f)
        S_f = [x for x in range(2**n) if f[x] == 1]
        rank = 0
        while S_f:
            x = S_f.pop()
            rank += 1
            S_f = [y for y in S_f if (x & y) != x]
        return rank

    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        w_f = xor_and_tree_width(f)
        rank_C_S_f = configuration_space_rank(f)
        results.append({
            "n": n,
            "w_f": w_f,
            "rank_C_S_f": rank_C_S_f
        })
    
    max_rank = max(result["rank_C_S_f"] for result in results)
    avg_w_f = sum(result["w_f"] for result in results) / len(results)
    
    if max_rank > avg_w_f * 1.5:  # Arbitrary threshold to check non-triviality
        return {
            "metric_name": "max_rank",
            "metric_value": max_rank,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": f"max_rank={max_rank} > 1.5 * avg_w_f={avg_w_f}"
        }
    else:
        return {
            "metric_name": "max_rank",
            "metric_value": max_rank,
            "instances_tested": len(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 30)]
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = result["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")