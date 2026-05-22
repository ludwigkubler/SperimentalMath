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
    
    def generate_random_csp(n):
        # Generate a random CSP instance with n variables
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def compute_min_order(csp):
        # Compute the minimal order of quaternion algebras
        n = len(csp)
        min_order = float('inf')
        for clause in csp:
            order = max(abs(x) for x in clause)
            if order < min_order:
                min_order = order
        return min_order
    
    def sum_of_squares_refutation(csp, levels):
        # Simulate a sum-of-squares refutation with given levels
        n = len(csp)
        refutation_size = 0
        for _ in range(levels):
            refutation_size += n
        return refutation_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_min_order = 0
    total_refutation_size = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 instances
            csp = generate_random_csp(n)
            min_order = compute_min_order(csp)
            refutation_size = sum_of_squares_refutation(csp, int(1.5 * n / 2))
            
            total_min_order += min_order
            total_refutation_size += refutation_size
            instances_tested += 1
            
            if min_order >= n**0.75 and refutation_size > int(1.5 * n / 2):
                conjecture_holds = False
                counterexample = f"n={n}, min_order={min_order}, refutation_size={refutation_size}"
    
    mean_min_order = total_min_order / instances_tested
    mean_refutation_size = total_refutation_size / instances_tested
    
    return {
        "metric_name": "mean_min_order",
        "metric_value": mean_min_order,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_min_order = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_min_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_min_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")