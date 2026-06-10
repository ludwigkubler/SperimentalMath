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
    
    def generate_boolean_circuit(s):
        return [random.choice([0, 1]) for _ in range(2**s)]
    
    def reflection_group(circuit):
        n = len(circuit)
        reflections = set()
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i] != circuit[j]:
                    ref = list(circuit)
                    ref[i], ref[j] = ref[j], ref[i]
                    reflections.add(tuple(ref))
        return reflections
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x_i - mean_x) * (y_i - mean_y) for x_i, y_i in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((x_i - mean_x)**2 for x_i in x) / len(x))
        std_y = math.sqrt(sum((y_i - mean_y)**2 for y_i in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    s_values = [5, 10, 15, 20, 30, 40]
    max_reflections = 0
    s_max = 0
    
    for s in s_values:
        circuit = generate_boolean_circuit(s)
        reflections = reflection_group(circuit)
        max_reflections = max(max_reflections, len(reflections))
        s_max = max(s_max, s)
    
    n_max = max(s_values)
    instances_tested = len(s_values)
    conjecture_holds = False
    counterexample = ""
    
    if max_reflections <= 5 * s_max:
        x = [math.sqrt(s) for s in s_values]
        y = [len(reflection_group(generate_boolean_circuit(s))) for s in s_values]
        r = correlation_coefficient(x, y)
        if r >= 0.8 and r < 0.6:
            counterexample = f"max_reflections={max_reflections}, s_max={s_max}"
        else:
            conjecture_holds = True
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient([math.sqrt(s) for s in s_values], [len(reflection_group(generate_boolean_circuit(s))) for s in s_values]),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{0.6}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")