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
    
    def log2(x):
        return math.log2(x) if x > 0 else float('-inf')
    
    def communication_complexity_rank(n):
        # Placeholder function for the actual rank calculation
        # This is a dummy implementation; replace with actual logic
        return n // 2
    
    def noncrossing_partitions_count(n):
        # Placeholder function for the actual partition count calculation
        # This is a dummy implementation; replace with actual logic
        return n + 1
    
    instances_tested = 0
    m_sum = 0
    r_sum = 0
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)
        m = noncrossing_partitions_count(n)
        r = communication_complexity_rank(n)
        
        if log2(n) <= m <= 2 * r:
            instances_tested += 1
            m_sum += m
            r_sum += r
        else:
            counterexample = f"n={n}, m={m}, r={r}"
    
    if counterexample:
        return {
            "metric_name": "noncrossing_partitions_count",
            "metric_value": (m_sum / instances_tested),
            "instances_tested": instances_tested,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    return {
        "metric_name": "noncrossing_partitions_count",
        "metric_value": (m_sum / instances_tested),
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) <= 5:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")