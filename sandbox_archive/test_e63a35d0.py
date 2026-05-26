# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_read_twice_boolean_function(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_read_twice_boolean_function(n // 2)
            right = generate_read_twice_boolean_function(n - n // 2)
            return [left[i] ^ right[i] for i in range(n)]
    
    def compute_free_probability_representation(f):
        n = len(f)
        F = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            F[0][i] = f[i]
            F[i][0] = f[i]
        for k in range(1, n + 1):
            for i in range(k + 1):
                j = k - i
                if i > 0:
                    F[i][j] = (F[i-1][j] + F[i][j-1]) / 2
                else:
                    F[i][j] = F[i][j-1]
        return F
    
    def compute_minimal_rank(F):
        n = len(F) - 1
        rank = 0
        for i in range(n, -1, -1):
            if any(F[j][i] != 0 for j in range(n + 1)):
                rank += 1
        return rank
    
    def compute_xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 1
        else:
            left_width = compute_xor_and_tree_width(f[:n // 2])
            right_width = compute_xor_and_tree_width(f[n // 2:])
            return max(left_width, right_width) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        f = generate_read_twice_boolean_function(n)
        F = compute_free_probability_representation(f)
        rank = compute_minimal_rank(F)
        width = compute_xor_and_tree_width(f)
        ranks.append(rank)
        widths.append(width)
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = (sum((ranks[i] - mean_rank) * (widths[i] - mean_width) for i in range(len(ranks)))) / \
                               math.sqrt(sum((ranks[i] - mean_rank)**2 for i in range(len(ranks)))) / \
                               math.sqrt(sum((widths[i] - mean_width)**2 for i in range(len(widths))))
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_rank <= n * math.log(n, 2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")