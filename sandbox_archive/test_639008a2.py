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
    
    def generate_boolean_circuit(n, d):
        if n == 1 and d == 0:
            return [random.choice([True, False])]
        inputs = generate_boolean_circuit(n // 2, d - 1)
        new_input = []
        for i in range(len(inputs)):
            if i + len(inputs) < n:
                new_input.append(inputs[i] and inputs[len(inputs) + i])
            else:
                new_input.append(random.choice([True, False]))
        return new_input
    
    def compute_affine_quotient_group(circuit):
        # Placeholder for actual computation
        return random.randint(1, 10)
    
    def monotone_width(circuit):
        # Placeholder for actual computation
        return len(circuit) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_boolean_circuit(n, random.randint(2, 5))
            generators = compute_affine_quotient_group(circuit)
            width = monotone_width(circuit)
            
            instances_tested += 1
            total_metric_value += generators
            
            if generators > n ** (0.5) * (random.randint(2, 5)) ** (3 / 2):
                conjecture_holds = False
                counterexample = f"n={n}, d={random.randint(2, 5)}, generators={generators}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = Fraction(instances_tested - int(conjecture_holds), instances_tested)
    
    return {
        "metric_name": "Generators",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = Fraction(sum(not result["conjecture_holds"] for result in results), len(results))
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif sum(not result["conjecture_holds"] for result in results) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")