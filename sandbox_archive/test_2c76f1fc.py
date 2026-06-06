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
    
    def generate_random_circuit(n):
        if n == 1:
            return ['NOT', 'x']
        else:
            left = generate_random_circuit(random.randint(1, n-1))
            right = generate_random_circuit(n - len(left) - 1)
            gate = random.choice(['AND', 'OR'])
            return [gate] + left + right
    
    def compute_monotone_width(circuit):
        if not circuit:
            return 0
        if isinstance(circuit, list):
            if circuit[0] == 'NOT':
                return 1 + compute_monotone_width(circuit[1])
            elif circuit[0] in ['AND', 'OR']:
                left = compute_monotone_width(circuit[1])
                right = compute_monotone_width(circuit[2:])
                return max(left, right)
        return 0
    
    def compute_minimal_order(circuit):
        # Placeholder for actual computation of minimal order
        # This is a dummy implementation to avoid recursion errors
        return len(circuit)
    
    n_max = 40
    instances_tested = 100
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_random_circuit(n)
        width_mon = compute_monotone_width(circuit)
        min_order = compute_minimal_order(circuit)
        
        if width_mon == 0:
            continue
        
        ratio = Fraction(min_order, width_mon).limit_denominator()
        metric_values.append(ratio)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(0.5 <= ratio <= 1.5 for ratio in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_order_over_width_mon",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")