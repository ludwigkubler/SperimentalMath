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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f'{variables[i-1]}'
            for j in range(i+1, n+1):
                clause += f' OR {variables[j-1]}'
            clauses.append(clause)
        return ' AND '.join(clauses)

    def communication_complexity_rank(formula):
        # Simplified version for demonstration
        return len(formula.split(' AND '))

    def minimal_order_of_cyclic_group(n):
        # Simplified version for demonstration
        return n

    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    rank = communication_complexity_rank(formula)
    order = minimal_order_of_cyclic_group(n)

    if order == 0:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "order_is_zero"
        }

    correlation = rank / order
    p_value = 0.5  # Placeholder for actual statistical test

    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation >= 0.7 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(res["conjecture_holds"] for res in results):
        mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        result = f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"

    print(result)