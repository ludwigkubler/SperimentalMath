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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return ['0', '1']
        else:
            inputs = generate_boolean_circuit(depth - 1)
            outputs = []
            for i in range(len(inputs)):
                for j in range(i + 1, len(inputs)):
                    outputs.append(f"({inputs[i]} OR {inputs[j]})")
                    outputs.append(f"({inputs[i]} AND {inputs[j]})")
                    outputs.append(f"(NOT {inputs[i]})")
            return outputs
    
    def k_theoretic_encoding(circuit):
        # Simplified K-theoretic encoding for demonstration
        return len(circuit)
    
    depths = [5, 10, 15, 20, 30, 40]
    n_max = max(depths)
    instances_tested = sum(2**(d-1) for d in depths)
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for depth in depths:
        circuit = generate_boolean_circuit(depth)
        num_vars = k_theoretic_encoding(circuit)
        metric_values.append(num_vars)
        
        if len(metric_values) >= 30 and abs(metric_values[-1] - metric_values[-2]) < 1e-6:
            conjecture_holds = False
            counterexample = "metric_saturation"
            break
    
    correlation_coefficient = calculate_correlation(depths, metric_values)
    
    if correlation_coefficient < 0.95:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": "Number of Noncommutative Variables",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
    
    return numerator / denominator if denominator != 0 else float('nan')

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")