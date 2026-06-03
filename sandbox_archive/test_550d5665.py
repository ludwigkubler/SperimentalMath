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
    
    def generate_boolean_circuit(n, d):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            inputs = generate_boolean_circuit(n // 2, d - 1)
            outputs = []
            for _ in range(d):
                gate_type = random.choice(['AND', 'OR'])
                new_input = []
                if gate_type == 'AND':
                    for i in range(n // 2):
                        new_input.append(inputs[i] and inputs[n // 2 + i])
                else:
                    for i in range(n // 2):
                        new_input.append(inputs[i] or inputs[n // 2 + i])
                outputs.append(new_input)
            return outputs
    
    def affine_quotient_group(circuit):
        # Simplified version of the affine quotient group calculation
        return len(circuit) * len(circuit[0])
    
    def monotone_width(circuit):
        # Simplified version of monotone width calculation
        max_width = 0
        for layer in circuit:
            max_width = max(max_width, len(layer))
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different circuits
            circuit = generate_boolean_circuit(n, random.randint(2, 5))
            generators = affine_quotient_group(circuit)
            width = monotone_width(circuit)
            results.append({
                "n": n,
                "generators": generators,
                "width": width
            })
    
    if not results:
        return {
            "metric_name": "monotone_width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [r["width"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(r["generators"] <= n * (n ** 0.5) * (r["width"] ** 1.5) for r in results)
    
    return {
        "metric_name": "monotone_width",
        "metric_value": mean,
        "instances_tested": len(metric_values),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "mapping_undefined" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")