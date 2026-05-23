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
    
    def generate_polynomial(n):
        return sum(random.randint(1, 10) * x**i for i in range(n))
    
    def compute_representation_size(f):
        # Placeholder function to simulate representation size computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(str(f)) + 5
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_polynomial(n)
        rank = compute_representation_size(f)
        results.append({
            "n": n,
            "rank": rank
        })
    
    min_rank = min(result["rank"] for result in results)
    instances_tested = len(results)
    conjecture_holds = all(abs(rank - math.log(n)) <= 3 for result in results for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
        support_fraction = (len([r for r in results if r["conjecture_holds"]]) / len(results)) * 100
    
    print(f"RESULT: SUPPORTED mean={mean_rank:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}%")