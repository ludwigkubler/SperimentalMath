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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        # Simplified decision tree construction
        if n == 1:
            return abs(f[0] - f[1])
        else:
            left = communication_complexity_rank([f[i] for i in range(2**(n-1))])
            right = communication_complexity_rank([f[i + 2**(n-1)] for i in range(2**(n-1))])
            return max(left, right) + 1
    
    def minimal_geometric_entropy(n):
        # Simplified geometric entropy calculation
        return n * math.log2(n)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        entropy = minimal_geometric_entropy(n)
        results.append((rank, entropy))
    
    if not results:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    ranks, entropies = zip(*results)
    correlation_coefficient = sum((ranks[i] - mean(ranks)) * (entropies[i] - mean(entropies)) for i in range(len(results))) / len(results) / math.sqrt(variance(ranks)) / math.sqrt(variance(entropies))
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": 0.5 < correlation_coefficient <= 0.7 and all(correlation_coefficient >= 0.5 for rank, entropy in results),
        "counterexample": "" if 0.5 < correlation_coefficient <= 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

def mean(lst):
    return sum(lst) / len(lst)

def variance(lst):
    avg = mean(lst)
    return sum((x - avg) ** 2 for x in lst) / len(lst)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(variance([r["metric_value"] for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")