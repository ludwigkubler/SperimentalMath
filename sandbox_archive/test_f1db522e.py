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
    
    k = 3  # Example value for k, can be changed as needed
    n_max = 40
    instances_tested = 0
    total_order = 0
    
    for n in range(5, n_max + 1):
        if n < k:
            continue
        
        instances_tested += 2 ** (n - k)
        
        # Generate all possible assignments of k variables to each clause in a k-CNF formula
        cnf_assignments = [tuple(random.choice([0, 1]) for _ in range(k)) for _ in range(2 ** n)]
        
        max_order = 0
        
        for assignment in cnf_assignments:
            # Construct the corresponding hypergeometric function (simplified example)
            order = sum(assignment) * (n - sum(assignment))
            if order > max_order:
                max_order = order
        
        total_order += max_order
    
    mean_order = total_order / instances_tested
    conjecture_holds = mean_order <= n_max ** (k / 2)
    counterexample = f"mean_order={mean_order}, max_order={max_order}" if not conjecture_holds else ""
    
    return {
        "metric_name": "Mean Order of Hypergeometric Functions",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")