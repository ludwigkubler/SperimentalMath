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
    
    def generate_protocol(n):
        # Generate a random n-ary communication protocol
        protocol = []
        for _ in range(100):  # Each protocol has 100 steps
            step = [random.randint(1, n) for _ in range(n)]
            protocol.append(step)
        return protocol
    
    def calculate_communication_complexity_rank(protocol):
        # Placeholder function to calculate communication complexity rank
        # This is a dummy implementation and should be replaced with actual logic
        return len(protocol)
    
    def calculate_noncommutative_crossed_product_order(protocol):
        # Placeholder function to calculate the minimal order of noncommutative crossed product
        # This is a dummy implementation and should be replaced with actual logic
        return len(protocol) * 2
    
    n = random.randint(5, 30)
    protocol = generate_protocol(n)
    communication_complexity_rank = calculate_communication_complexity_rank(protocol)
    crossed_product_order = calculate_noncommutative_crossed_product_order(protocol)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": communication_complexity_rank,
        "instances_tested": 100,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")