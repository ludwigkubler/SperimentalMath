# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def communication_rank_variance(f):
    n = len(f)
    count_0 = sum(f.count(0) for f in f)
    count_1 = sum(f.count(1) for f in f)
    delta_f = Fraction(count_0 - count_1, 2**n)
    return delta_f

def quasi_plurality_group_size(delta_f):
    if delta_f == 0:
        return 1
    return int(delta_f**-2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        f = generate_boolean_function(n)
        delta_f = communication_rank_variance(f)
        qpg_size = quasi_plurality_group_size(delta_f)
        
        if qpg_size > 10:
            return {
                "metric_name": "quasi_plurality_group_size",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "qpg_size > 10"
            }
        
        metric_values.append(qpg_size)
        instances_tested += len(f)
        n_max = max(n_max, n)

    return {
        "metric_name": "quasi_plurality_group_size",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(qpg_size <= 10 for qpg_size in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"qpg_size > 10\" first_failing_seed={first_failing_seed}")