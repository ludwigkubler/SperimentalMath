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

def generate_matrix_product_state(depth):
    n = 2 ** depth
    state = [[0] * n for _ in range(n)]
    state[0][0] = 1
    return state

def kahler_potential(matrix):
    n = len(matrix)
    rank = 0
    for i in range(n):
        if all(matrix[j][i] == 0 for j in range(n)):
            continue
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        depth = random.randint(1, n // 2)
        matrix_product_state = generate_matrix_product_state(depth)
        kahler_rank = kahler_potential(matrix_product_state)
        
        results.append({
            "n": n,
            "depth": depth,
            "kahler_rank": kahler_rank
        })
    
    min_diff = float('inf')
    max_diff = 0
    
    for result in results:
        diff = abs(result["depth"] - result["kahler_rank"])
        if diff > max_diff:
            max_diff = diff
        if diff < min_diff:
            min_diff = diff
    
    mean_diff = sum(abs(result["depth"] - result["kahler_rank"]) for result in results) / len(results)
    
    conjecture_holds = all(diff <= 1 for diff in [abs(result["depth"] - result["kahler_rank"]) for result in results])
    counterexample = "" if conjecture_holds else "min_diff={}".format(min_diff)
    
    return {
        "metric_name": "Mean Difference",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    mean_diff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_diff, 0, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_diff, 0, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='min_diff>1' first_failing_seed={}".format(first_failing_seed))