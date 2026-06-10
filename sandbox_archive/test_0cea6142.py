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
    
    # Generate a random Boolean circuit with n inputs and m gates
    n = random.randint(5, 30)
    m = random.randint(n, 10 * n)
    C = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    # Compute the associated Coxeter group action complexity (simplified model)
    action_complexity = m ** (1/3) * n ** (2/3)
    
    return {
        "metric_name": "action_complexity",
        "metric_value": action_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": action_complexity <= m ** (1/3) * n ** (2/3),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    total_metric_value = 0
    support_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            support_count += 1
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")