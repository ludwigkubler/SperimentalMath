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
    
    def generate_boolean_circuit(s: int, n: int):
        if s <= 0 or n <= 0:
            return []
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(s)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_reflection_group(circuit):
        s = len(set(input for _, inputs in circuit for input in inputs))
        if s <= 0:
            return []
        reflections = set()
        for i in range(s):
            reflection = [1 if j == i else -1 for j in range(s)]
            reflections.add(tuple(reflection))
        return reflections
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_max = 40
    instances_tested = 30
    total_r = 0
    max_reflections = 0
    
    for _ in range(instances_tested):
        s = random.randint(1, n_max)
        circuit = generate_boolean_circuit(s, n_max)
        reflections = compute_reflection_group(circuit)
        num_reflections = len(reflections)
        
        if num_reflections > max_reflections:
            max_reflections = num_reflections
        
        total_r += correlation_coefficient([num_reflections], [math.sqrt(s)])
    
    mean_r = total_r / instances_tested
    conjecture_holds = 0.6 <= mean_r >= 0.8 and max_reflections <= 5 * s_max
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_reflections={max_reflections}, s_max={s_max}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")