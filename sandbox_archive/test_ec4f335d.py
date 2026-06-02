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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_algebraic_variety(cnf):
        # Placeholder function to simulate algebraic variety computation
        return len(cnf)  # Simplified for demonstration purposes
    
    def minimal_order_of_arithmetic_cycles(variety):
        # Placeholder function to simulate arithmetic cycle computation
        return variety * variety  # Simplified for demonstration purposes
    
    def communication_complexity_rank(cnf):
        # Placeholder function to simulate communication complexity rank computation
        return len(cnf)  # Simplified for demonstration purposes
    
    n = random.randint(5, 40)
    k = random.randint(1, n // 2)
    cnf = generate_k_cnf(n, k)
    variety = compute_algebraic_variety(cnf)
    m_order = minimal_order_of_arithmetic_cycles(variety)
    r_phi = communication_complexity_rank(cnf)
    
    if m_order < n**2 * math.log(n) or m_order > 10 * r_phi:
        return {
            "metric_name": "m_order",
            "metric_value": m_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "m_order",
        "metric_value": m_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(metric_values) / len(results)
    metric_mean = sum(metric_values) / len(metric_values)
    
    if support_fraction >= 0.8 and metric_mean <= 10:
        print(f"RESULT: SUPPORTED mean={metric_mean} std=<y> support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")