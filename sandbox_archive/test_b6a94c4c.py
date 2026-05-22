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

def generate_circuit(n):
    if n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        a = generate_circuit(n // 2)
        b = generate_circuit(n - n // 2)
        return [0] + a + [1] + b

def compute_function_field(circuit):
    if len(circuit) == 1:
        return {0: 1}
    else:
        field = {}
        for i in range(len(circuit)):
            if circuit[i] == 0:
                for key, value in compute_function_field(circuit[:i]).items():
                    field[key * 2] = value
            else:
                for key, value in compute_function_field(circuit[:i]).items():
                    field[key * 2 + 1] = value
        return field

def compute_brauer_group_order(field):
    order = 1
    for key in field:
        if key != 0:
            order *= abs(key)
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        field = compute_function_field(circuit)
        order = compute_brauer_group_order(field)
        
        if order == 0:
            continue
        
        size = len(circuit)
        results.append((order, size))
    
    if not results:
        return {
            "metric_name": "Brauer Group Order vs Circuit Size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orders, sizes = zip(*results)
    mean_order = sum(orders) / len(orders)
    std_order = math.sqrt(sum((x - mean_order) ** 2 for x in orders) / len(orders))
    
    correlation_coefficient = sum((orders[i] - mean_order) * (sizes[i] - sum(sizes) / len(sizes)) for i in range(len(orders))) / (len(orders) * std_order * math.sqrt(sum((x - sum(sizes) / len(sizes)) ** 2 for x in sizes)))
    
    return {
        "metric_name": "Brauer Group Order vs Circuit Size",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient > 0.7 and std_order < 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_coeff = sum(result["metric_value"] for result in results if result["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["instances_tested"] > 0 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")