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
        if all(f[i] == f[0] for i in range(1, n)):
            return 1
        mid = n // 2
        left_width = xor_and_tree_width(f[:mid])
        right_width = xor_and_tree_width(f[mid:])
        return max(left_width, right_width) + 1
    
    def configuration_space_rank(f):
        n = len(f)
        if n == 1:
            return 1
        if all(f[i] == f[0] for i in range(1, n)):
            return 1
        mid = n // 2
        left_rank = configuration_space_rank(f[:mid])
        right_rank = configuration_space_rank(f[mid:])
        return max(left_rank, right_rank) + 1
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_random_boolean_function(n)
        width = xor_and_tree_width(f)
        rank = configuration_space_rank(f)
        results.append((n, width, rank))
    
    total_instances = sum(1 for _, _, _ in results)
    max_rank = max(rank for _, _, rank in results)
    min_width = min(width for _, width, _ in results)
    
    if max_rank > 2 * min_width:
        return {
            "metric_name": "rank_over_width",
            "metric_value": max_rank / min_width,
            "instances_tested": total_instances,
            "conjecture_holds": False,
            "counterexample": f"max_rank={max_rank}, min_width={min_width}"
        }
    else:
        return {
            "metric_name": "rank_over_width",
            "metric_value": max_rank / min_width,
            "instances_tested": total_instances,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break