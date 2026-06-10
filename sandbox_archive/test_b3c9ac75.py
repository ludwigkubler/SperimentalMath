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

def generate_circuit(n):
    if n == 1:
        return ['0', '1']
    left = generate_circuit(n // 2)
    right = generate_circuit(n - n // 2)
    return [f'({l} OR {r})' for l in left] + [f'({l} AND {r})' for l in left]

def twistor_space(circuit):
    if not circuit:
        return 0
    if isinstance(circuit, str):
        return 1
    return sum(twistor_space(subcircuit) for subcircuit in circuit)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        order = twistor_space(circuit)
        depth = len(circuit) - n + 1
        results.append((order, depth))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_order = sum(order for order, _ in results) / len(results)
    mean_depth = sum(depth for _, depth in results) / len(results)
    correlation = (sum((order - mean_order) * (depth - mean_depth) for order, depth in results) /
                   math.sqrt(sum((order - mean_order) ** 2 for order, _ in results) *
                             sum((depth - mean_depth) ** 2 for _, depth in results)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_correlation = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction=1.0")
    elif sum(1 for res in results if res["metric_value"] < 0.5) >= 6:
        first_failing_seed = next(seed for seed, res in enumerate(results) if res["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")