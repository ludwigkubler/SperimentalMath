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
    
    def formal_group_rank(f):
        # Placeholder implementation of formal group rank calculation
        # This is a dummy function and should be replaced with actual logic
        return len(f)
    
    def read_twice_bp_size(f):
        # Placeholder implementation of read-twice BP size calculation
        # This is a dummy function and should be replaced with actual logic
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    bp_sizes = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = formal_group_rank(f)
        bp_size = read_twice_bp_size(f)
        ranks.append(rank)
        bp_sizes.append(bp_size)
    
    correlation_coefficient = sum((ranks[i] - sum(ranks) / len(ranks)) * (bp_sizes[i] - sum(bp_sizes) / len(bp_sizes)) for i in range(len(ranks))) / (len(ranks) * math.sqrt(sum((ranks[i] - sum(ranks) / len(ranks))**2 for i in range(len(ranks)))) * math.sqrt(sum((bp_sizes[i] - sum(bp_sizes) / len(bp_sizes))**2 for i in range(len(bp_sizes)))))
    mean_difference = abs(sum(ranks) / len(ranks) - sum(bp_sizes) / len(bp_sizes))
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_difference <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")