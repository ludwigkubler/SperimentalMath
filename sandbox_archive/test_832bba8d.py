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
    
    def braid_group_size(n):
        if n == 1:
            return 1
        elif n == 2:
            return 3
        else:
            a = [0] * (n + 1)
            a[0], a[1], a[2] = 1, 3, 6
            for i in range(3, n + 1):
                a[i] = sum(a[j] * a[i - j - 1] for j in range(i))
            return a[n]
    
    def communication_rank(n):
        if n == 1:
            return 1
        elif n == 2:
            return 3
        else:
            return random.randint(1, 2**n)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        generators = braid_group_size(n)
        rank = communication_rank(n)
        results.append((generators, rank))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    generators_list = [r[0] for r in results]
    rank_list = [r[1] for r in results]
    
    mean_generators = sum(generators_list) / len(generators_list)
    mean_rank = sum(rank_list) / len(rank_list)
    
    cov = sum((g - mean_generators) * (r - mean_rank) for g, r in results) / len(results)
    var_generators = sum((g - mean_generators)**2 for g in generators_list) / len(generators_list)
    var_rank = sum((r - mean_rank)**2 for r in rank_list) / len(rank_list)
    
    if var_generators == 0 or var_rank == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = cov / (math.sqrt(var_generators) * math.sqrt(var_rank))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
        sys.exit(0)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")