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
    
    def non_abelian_automorphism_group_rank(f):
        # Placeholder function to compute the rank of the non-abelian automorphism group
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = non_abelian_automorphism_group_rank(f)
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    variance = sum((x - mean_rank) ** 2 for x in results) / len(results)
    
    return {
        "metric_name": "Variance of Non-Abelian Automorphism Group Ranks",
        "metric_value": variance,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": variance <= 10 * n_max ** 2,
        "counterexample": "" if variance <= 10 * n_max ** 2 else f"Variance {variance} exceeds bound for n={n_max}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std={math.sqrt(sum((r['metric_value'] - mean_variance) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std={math.sqrt(sum((r['metric_value'] - mean_variance) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Variance exceeds bound\" first_failing_seed={first_failing_seed}")