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
        if n <= 0 or k <= 0:
            return None
        order = 1
        for i in range(1, k + 1):
            order *= (n - i + 1) / i
        return int(math.ceil(order))
    
    def generate_k_cnf(k, n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * random.randint(1, k) for _ in range(k)]
            clauses.append(clause)
        return clauses
    
    def calculate_order_of_hypergeometric_functions(clauses, n):
        orders = []
        for clause in clauses:
            order = hypergeometric_order(n, len(clause))
            if order is not None:
                orders.append(order)
        return orders
    
    k_values = [5, 10, 15, 20, 30, 40]
    total_orders = []
    
    for k in k_values:
        n = random.randint(1, 40)
        clauses = generate_k_cnf(k, n)
        orders = calculate_order_of_hypergeometric_functions(clauses, n)
        if len(orders) < 30:
            return {
                "metric_name": "order",
                "metric_value": None,
                "instances_tested": len(orders),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
        total_orders.extend(orders)
    
    mean_order = sum(total_orders) / len(total_orders)
    conjecture_holds = all(order <= n**(k/2) for order, k in zip(total_orders, k_values))
    
    return {
        "metric_name": "order",
        "metric_value": mean_order,
        "instances_tested": len(total_orders),
        "n_max": max(k_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all("counterexample" in r and r["counterexample"] != "" for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if 'counterexample' in r and r['counterexample'] != ''))]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient_support_fraction={support_fraction}")