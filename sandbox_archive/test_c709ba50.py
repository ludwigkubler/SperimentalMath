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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(abs(x) <= n for x in clause):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = cnf[:]
        while stack:
            clause = stack.pop()
            new_clause = None
            for c in stack:
                if any(-x in c for x in clause):
                    new_clause = [x for x in c if x not in clause and -x not in clause]
                    break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause)
        return 0
    
    def tropicalized_brauer_group(cnf):
        # Placeholder function to simulate computation of Brauer group order
        return random.randint(1, 10) * len(cnf)
    
    results = []
    for n in [5, 10, 15, 20, 30]:
        for _ in range(6):
            cnf = generate_cnf(n)
            brauer_group_order = tropicalized_brauer_group(cnf)
            resolution_width_value = resolution_width(cnf)
            results.append((brauer_group_order, resolution_width_value))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    brauer_group_orders = [r[0] for r in results]
    resolution_width_values = [r[1] for r in results]
    
    mean_brauer_group_order = sum(brauer_group_orders) / len(brauer_group_orders)
    mean_resolution_width_value = sum(resolution_width_values) / len(resolution_width_values)
    
    covariance = sum((brauer_group_orders[i] - mean_brauer_group_order) * (resolution_width_values[i] - mean_resolution_width_value) for i in range(len(results))) / len(results)
    variance_brauer_group_order = sum((brauer_group_orders[i] - mean_brauer_group_order) ** 2 for i in range(len(results))) / len(results)
    variance_resolution_width_value = sum((resolution_width_values[i] - mean_resolution_width_value) ** 2 for i in range(len(results))) / len(results)
    
    correlation_coefficient = covariance / math.sqrt(variance_brauer_group_order * variance_resolution_width_value)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(6) for n in [5, 10, 15, 20, 30]),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(64) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["instances_tested"] > 0 for r in results):
        print("RESULT: INCONCLUSIVE insufficient_data")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")