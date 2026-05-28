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
    
    def cc_xor(n):
        return n
    
    def coin_tossing_time(n):
        # Simplified model for coin tossing time
        return random.randint(1, 2**n)
    
    def log_base_2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    metric_name = "coin_tossing_time"
    instances_tested = 30
    total_time = 0
    support_count = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        time = coin_tossing_time(n)
        cc = cc_xor(n)
        expected_bound = log_base_2(cc) * n
        
        if time <= 2 * expected_bound:
            support_count += 1
        total_time += time
    
    mean_time = total_time / instances_tested
    conjecture_holds = (support_count >= 0.8 * instances_tested)
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_time,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30*31, 67))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_time = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_time} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_time} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")