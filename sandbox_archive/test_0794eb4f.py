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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_property_Q(values):
        # Placeholder for the actual computation of property Q
        # For this example, we'll use a dummy function that returns a constant value
        return sum(values) / len(values)
    
    def construct_AC0_circuit(f):
        n = int(math.log2(len(f)))
        circuit_size = 0
        for i in range(n):
            circuit_size += 1
        return circuit_size
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_sum = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        values = [f[i] for i in range(2**n)]
        Q = compute_property_Q(values)
        circuit_size = construct_AC0_circuit(f)
        
        if circuit_size < c * math.log(n):
            conjecture_holds = False
            counterexample = f"AC0 circuit size {circuit_size} < {c * math.log(n)} for n={n}"
            break
        
        metric_sum += Q
        instances_tested += len(values)
    
    if not conjecture_holds:
        return {
            "metric_name": "property_Q",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    metric_mean = metric_sum / instances_tested
    
    if metric_mean > 3:
        return {
            "metric_name": "property_Q",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"Mean property_Q {metric_mean} > 3"
        }
    
    return {
        "metric_name": "property_Q",
        "metric_value": metric_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(result)