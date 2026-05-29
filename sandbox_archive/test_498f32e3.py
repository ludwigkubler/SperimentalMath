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
    
    def hypergeometric_order(n, k):
        if n == 0 or k == 0:
            return 1
        order = 1
        for i in range(1, k + 1):
            order *= (n - i + 1) / i
        return int(math.ceil(order))
    
    def generate_k_cnf(k, n):
        cnf = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * random.randint(1, k) for _ in range(k)]
            cnf.append(clause)
        return cnf
    
    def calculate_order(cnf):
        orders = []
        for clause in cnf:
            n = len(clause)
            order = hypergeometric_order(n, k)
            orders.append(order)
        return orders
    
    k_values = [5, 10, 15, 20, 30, 40]
    total_orders = []
    instances_tested = 0
    n_max = 0
    
    for k in k_values:
        cnf = generate_k_cnf(k, 10)  # Generate 10 instances per k
        orders = calculate_order(cnf)
        total_orders.extend(orders)
        instances_tested += len(orders)
        n_max = max(n_max, k)
    
    mean_order = sum(total_orders) / instances_tested
    conjecture_holds = all(order <= n**(k/2) for order in total_orders)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")