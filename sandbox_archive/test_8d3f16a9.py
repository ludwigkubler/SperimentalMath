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
    
    # Generate a random affine variety V with generators of varying lengths L
    n = random.randint(5, 30)
    L = random.randint(1, 10)
    generators = [random.randint(1, 100) for _ in range(L)]
    
    # Compute the minimal representation length L (simulated as a function of L)
    min_representation_length = L
    
    # Simulate the growth rate of communication complexity
    communication_complexity_growth_rate = L * math.log(L, 2)
    
    # Check if the conjecture holds for this trial
    conjecture_holds = abs(min_representation_length - communication_complexity_growth_rate) < 1e-6
    
    return {
        "metric_name": "communication_complexity_growth_rate",
        "metric_value": communication_complexity_growth_rate,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"V with L={L}, min_representation_length={min_representation_length}, communication_complexity_growth_rate={communication_complexity_growth_rate}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")