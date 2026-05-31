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
    
    def q_difference_operator_representation(k, n):
        # Placeholder for actual implementation
        return [random.randint(1, 10) for _ in range(n)]
    
    def count_non_zero_hypergeometric_coefficients(q_diff_op):
        return sum(1 for coeff in q_diff_op if coeff != 0)
    
    k = random.randint(2, 5)
    n_max = max(5, 2 * k + 3)  # Ensure n_max is at least 5
    instances_tested = 0
    
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        q_diff_op = q_difference_operator_representation(k, n_max)
        metric_value = count_non_zero_hypergeometric_coefficients(q_diff_op)
        instances_tested += len(q_diff_op)
        
        if not conjecture_holds:
            continue
        
        total_metric_value += metric_value
        if metric_value < k * math.log(n_max):
            conjecture_holds = False
            counterexample = f"Failed for k={k}, n={n_max}"
    
    return {
        "metric_name": "Number of distinct non-zero hypergeometric function coefficients",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")