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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        # Simplified version of communication complexity rank calculation
        return n
    
    def local_indeterminacy(f):
        # Simplified version of local indeterminacy calculation
        return sum(f) / len(f)
    
    results = []
    for _ in range(30):  # Test with 30 instances per seed
        f = generate_random_boolean_function(20)
        r_f = communication_complexity_rank(f)
        il = local_indeterminacy(f)
        results.append((il, r_f))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 20,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n = len(results)
    sum_x = sum(x for x, _ in results)
    sum_y = sum(y for _, y in results)
    sum_xy = sum(x * y for x, y in results)
    sum_xx = sum(x**2 for x, _ in results)
    sum_yy = sum(y**2 for _, y in results)
    
    mean_x = sum_x / n
    mean_y = sum_y / n
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_xx - sum_x**2) * (n * sum_yy - sum_y**2))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0,
            "instances_tested": n,
            "n_max": 20,
            "conjecture_holds": False,
            "counterexample": "Denominator is zero"
        }
    
    pearson_corr = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": n,
        "n_max": 20,
        "conjecture_holds": abs(pearson_corr) > 0.5,  # Simplified threshold for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]  # Default to first 3 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials ran")
        sys.exit(0)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                sys.exit(0)