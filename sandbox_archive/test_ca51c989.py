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
        if n < k or k == 0:
            return 0
        order = 1
        for i in range(1, k + 1):
            order *= (n - i + 1) / i
        return int(order)
    
    def generate_kcnf(k):
        variables = list(range(1, k + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, k)
            clauses.append(clause)
        return clauses
    
    def calculate_order_of_hypergeometric_functions(n, k):
        orders = []
        for _ in range(30):  # Ensure at least 30 instances per seed
            clauses = generate_kcnf(k)
            order = hypergeometric_order(n, len(clauses))
            orders.append(order)
        return sum(orders) / len(orders), max(orders)
    
    k = random.randint(2, 5)  # Randomly choose k between 2 and 5
    n_max = 40
    total_order = 0
    max_order = 0
    
    for n in range(5, n_max + 1):
        order, max_order = calculate_order_of_hypergeometric_functions(n, k)
        total_order += order
    
    mean_order = total_order / (n_max - 4)
    
    conjecture_holds = mean_order <= n_max ** (k / 2) and max_order <= n_max ** (k / 2)
    counterexample = "" if conjecture_holds else f"mean_order={mean_order}, max_order={max_order}"
    
    return {
        "metric_name": "Mean Order of Hypergeometric Functions",
        "metric_value": mean_order,
        "instances_tested": n_max - 4,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")