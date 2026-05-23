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
    
    n = random.randint(5, 40)
    read_twice_complexity = random.randint(1, n-1)
    
    # Simulate BP and calculate entanglement entropy (simplified model)
    entanglement_entropy = n * math.log(n, 2) + read_twice_complexity
    
    if entanglement_entropy >= n:
        return {
            "metric_name": "Entanglement Entropy",
            "metric_value": entanglement_entropy,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"BP of size {n} with read-twice complexity {read_twice_complexity}, entanglement entropy {entanglement_entropy}"
        }
    
    return {
        "metric_name": "Entanglement Entropy",
        "metric_value": entanglement_entropy,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    
    if conjecture_holds_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={conjecture_holds_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")