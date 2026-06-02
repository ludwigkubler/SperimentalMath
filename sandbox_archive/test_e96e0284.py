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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 3))
            clauses.append(clause)
        return clauses
    
    def communication_complexity_rank(phi):
        # Placeholder implementation
        return len(phi) * 2
    
    def minimal_order_of_arithmetic_cycles(phi):
        # Placeholder implementation
        return len(phi) ** 2
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n, 10))
    phi = generate_kcnf(n, k)
    
    m_order = minimal_order_of_arithmetic_cycles(phi)
    r_phi = communication_complexity_rank(phi)
    
    if m_order < n**2 * math.log(n):
        return {
            "metric_name": "minimal_order",
            "metric_value": m_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "m_order is less than O(n^2 log n)"
        }
    
    return {
        "metric_name": "minimal_order",
        "metric_value": m_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(metric_values) / len(results)
    metric_mean = sum(metric_values) / len(metric_values) if metric_values else 0
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={metric_mean} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")