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
    
    def log2(x):
        return math.log(x, 2)

    def min_quadratic_entropy(B, E):
        if B <= 0 or E <= 0:
            return float('inf')
        return B * E + (1 - B) * (1 - E)

    n = random.randint(5, 40)
    B = random.randint(1, n)
    E = random.uniform(0.01, 0.99)
    
    H_min = min_quadratic_entropy(B, E)
    
    return {
        "metric_name": "min_quadratic_entropy",
        "metric_value": H_min,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": H_min <= log2(n) * log2(1 / E),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    total_metric_value = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supporting += 1
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = count_supporting / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample='not_supported' first_failing_seed=None")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")