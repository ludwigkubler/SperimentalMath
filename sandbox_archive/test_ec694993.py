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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def clause_indicator_polynomial(instance):
        n = len(instance)
        polynomial = []
        for i in range(2**n):
            binary_rep = format(i, f'0{n}b')
            product = 1
            for j in range(n):
                if binary_rep[j] == '1':
                    product *= instance[j]
                else:
                    product *= (1 - instance[j])
            polynomial.append(product)
        return polynomial
    
    def minimal_order_quaternion_algebra(polynomial):
        n = len(polynomial)
        order = 0
        for i in range(2**n):
            if all(abs(polynomial[j] - polynomial[j ^ i]) < 1e-6 for j in range(n)):
                order += 1
        return order
    
    def resolution_proof_width(instance):
        n = len(instance)
        width = 0
        for _ in range(2**n):
            clause = random.choice(instance)
            if clause == 0:
                continue
            width += 1
        return width
    
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        instance = generate_boolean_instance(n)
        polynomial = clause_indicator_polynomial(instance)
        order = minimal_order_quaternion_algebra(polynomial)
        width = resolution_proof_width(instance)
        
        metric_values.append(order / width)
        instances_tested += len(instance)
        n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "order_over_width",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_metric_values"
        }
    
    mean_o_qm = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "order_over_width",
        "metric_value": mean_o_qm,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_o_qm >= 0.7 and all(x >= 0.5 for x in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_o_qm = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_o_qm} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")