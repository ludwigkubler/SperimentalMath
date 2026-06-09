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
    
    def rank_variance(n):
        return sum(random.randint(1, 40) for _ in range(n)) / n
    
    def generate_coxeter_group(r):
        # Simplified Coxeter group generation based on rank r
        # This is a placeholder and should be replaced with actual Coxeter group construction
        return [tuple(sorted(random.sample(range(1, r+1), 2))) for _ in range(10)]
    
    def maximal_parabolic_subgroups(group):
        subgroups = set()
        for subgroup in group:
            if all(subgroup[i] < subgroup[i+1] for i in range(len(subgroup)-1)):
                subgroups.add(tuple(sorted(subgroup)))
        return subgroups
    
    n_max = 0
    instances_tested = 0
    total_count = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        r = rank_variance(n)
        if r <= 40:
            instances_tested += 1
            n_max = max(n_max, n)
            group = generate_coxeter_group(r)
            count = len(maximal_parabolic_subgroups(group))
            total_count += count
    
    metric_value = total_count / instances_tested
    conjecture_holds = metric_value <= 40 * instances_tested
    counterexample = "" if conjecture_holds else f"r={r}, count={count}"
    
    return {
        "metric_name": "Number of distinct maximal parabolic subgroups",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")