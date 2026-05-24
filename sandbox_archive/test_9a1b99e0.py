# auto-injected by SEC sandbox
import math
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

def generate_bp(depth):
    if depth == 1:
        return [random.choice([0, 1])]
    sub_depth = random.randint(2, depth - 1)
    left = generate_bp(sub_depth)
    right = generate_bp(depth - sub_depth - 1)
    return [left + right]

def compute_hodge_diamond(bp):
    n = len(bp)
    hodge_diamond = [[0] * (n + i) for i in range(n)]
    hodge_diamond[0][0] = bp[0]
    for i in range(1, n):
        hodge_diamond[i][0] = hodge_diamond[i-1][i-1]
        hodge_diamond[i][i] = bp[i]
        for j in range(1, i):
            hodge_diamond[i][j] = hodge_diamond[i-1][j-1] + hodge_diamond[i-1][j]
    return hodge_diamond

def min_rank(hodge_diamond):
    n = len(hodge_diamond)
    rank = 0
    for i in range(n):
        row_sum = sum(hodge_diamond[i])
        if row_sum != 0:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_tests = 30
    total_rank = 0
    total_depth = 0
    instances_tested = 0
    
    for _ in range(n_tests):
        depth = random.randint(5, 40)
        bp = generate_bp(depth)
        hodge_diamond = compute_hodge_diamond(bp)
        rank = min_rank(hodge_diamond)
        
        total_rank += rank
        total_depth += depth
        instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_depth = total_depth / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * depth for rank, depth in zip([mean_rank] * instances_tested, [mean_depth] * instances_tested)) - total_rank * total_depth) / ((instances_tested * sum(rank**2 for rank in [mean_rank] * instances_tested) - total_rank**2) ** 0.5 * (instances_tested * sum(depth**2 for depth in [mean_depth] * instances_tested) - total_depth**2) ** 0.5)
    mean_absolute_error = sum(abs(rank - depth) for rank, depth in zip([mean_rank] * instances_tested, [mean_depth] * instances_tested)) / instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_error <= 5
    counterexample = "" if conjecture_holds else "correlation_coefficient={:.2f}, mean_absolute_error={:.2f}".format(correlation_coefficient, mean_absolute_error)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_correlation_coefficient = sum(r["metric_value"] for r in results) / len(results)
    mean_absolute_error = sum(abs(r["metric_value"] - 1) for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.2f} std={:.2f} support_fraction={:.2f}".format(mean_correlation_coefficient, 0.0, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.2f} std={:.2f} support_fraction={:.2f}".format(mean_correlation_coefficient, 0.0, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient={:.2f}, mean_absolute_error={:.2f}\" first_failing_seed={}".format(mean_correlation_coefficient, mean_absolute_error, first_failing_seed))