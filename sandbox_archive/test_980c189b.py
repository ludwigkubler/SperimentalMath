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
            return ['0'] if random.choice([True, False]) else ['1']
        if depth == 1:
            return [random.choice(['NOT', 'AND', 'OR'])]
        op = random.choice(['NOT', 'AND', 'OR'])
        left = generate_boolean_circuit(depth - 1)
        right = generate_boolean_circuit(depth - 1)
        return [op, left, right]
    
    def count_noncommutative_variables(circuit):
        if isinstance(circuit, list):
            if circuit[0] in ['NOT', 'AND', 'OR']:
                return sum(count_noncommutative_variables(sub) for sub in circuit[1:])
            else:
                return 1
        return 0
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    depths = [5, 10, 15, 20, 30, 40]
    num_vars = []
    depths_tested = 0
    
    for depth in depths:
        circuit = generate_boolean_circuit(depth)
        num_vars.append(count_noncommutative_variables(circuit))
        depths_tested += 1
        if depths_tested >= 30:
            break
    
    n_max = max(depths)
    metric_value = correlation_coefficient(num_vars, depths)
    
    conjecture_holds = abs(metric_value) >= 0.95
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.95"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": metric_value,
        "instances_tested": depths_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.95\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")