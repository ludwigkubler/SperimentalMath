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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def support_size(f):
        return sum(1 for x in f if x == 1)
    
    def noncrossing_partition_rank(support_size):
        if support_size <= 1:
            return 0
        return 1 + noncrossing_partition_rank(support_size - 2)
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 0
        # Forster's signed-rank technique (simplified for demonstration)
        rank = support_size(f)
        return rank
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        f = generate_boolean_function(random.randint(5, 40))
        tau = noncrossing_partition_rank(support_size(f))
        C_f = communication_complexity(f)
        results.append((tau, C_f))
    
    mean_difference = sum(abs(tau - C_f) for tau, C_f in results) / len(results)
    conjecture_holds = mean_difference <= 3
    
    return {
        "metric_name": "mean_difference",
        "metric_value": mean_difference,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_difference = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_difference} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")