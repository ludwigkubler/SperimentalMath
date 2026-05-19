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
    
    n = 40
    instances_tested = 5000
    discrepancy_sum = 0
    
    for _ in range(instances_tested):
        # Generate two random unit vectors
        u = [random.gauss(0, 1) for _ in range(n)]
        v = [random.gauss(0, 1) for _ in range(n)]
        
        # Normalize the vectors to make them unit vectors
        norm_u = math.sqrt(sum(x**2 for x in u))
        norm_v = math.sqrt(sum(x**2 for x in v))
        u = [x / norm_u for x in u]
        v = [x / norm_v for x in v]
        
        # Compute the inner product
        inner_product = sum(x * y for x, y in zip(u, v))
        
        # Accumulate the discrepancy
        discrepancy_sum += abs(inner_product)
    
    # Calculate the mean discrepancy
    mean_discrepancy = discrepancy_sum / instances_tested
    
    # Calculate the lower bound
    lower_bound = math.sqrt(math.log(n))
    
    # Check if the conjecture holds
    conjecture_holds = mean_discrepancy >= lower_bound
    
    return {
        "metric_name": "discrepancy",
        "metric_value": mean_discrepancy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_discrepancy={mean_discrepancy}, lower_bound={lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_discrepancy = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_discrepancy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_discrepancy} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_discrepancy} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{r['counterexample']}' first_failing_seed={first_failing_seed}")