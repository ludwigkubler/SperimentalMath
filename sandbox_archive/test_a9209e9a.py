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
    
    def compute_l_function(f):
        n = int(math.log2(len(f)))
        if f == [0]*len(f):
            return 1
        count = sum(1 for i in range(n) if all(f[j] == f[i] for j in range(i+1, len(f), 2**i)))
        return count
    
    def min_rank_l_function(f):
        n = int(math.log2(len(f)))
        rank = float('inf')
        for d in range(1, n + 1):
            for s in range(1, 2**(n-d) + 1):
                if len([i for i in range(n) if f[i] == f[(i + s) % (2**d)]]) >= s:
                    rank = min(rank, d * math.log(s)**2)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        l_function_rank = min_rank_l_function(f)
        results.append({
            "n": n,
            "l_function_rank": l_function_rank
        })
    
    mean_rank = sum(result["l_function_rank"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["l_function_rank"] - mean_rank)**2 for result in results) / len(results))
    
    conjecture_holds = all(mean_rank >= 0.5 * math.log(n) and mean_rank <= 1.5 * math.log(n) for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank_l_function",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")