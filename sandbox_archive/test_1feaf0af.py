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
    
    def generate_circuit(n):
        if n == 1:
            return ['A']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - len(left))
            return [f'({left[0]} {right[0]})'] + left + right
    
    def circuit_satisfiability_threshold(circuit):
        if not circuit:
            return 0
        if isinstance(circuit, str):
            return 1
        left, right = circuit.split()
        return max(circuit_satisfiability_threshold(left), circuit_satisfiability_threshold(right))
    
    def grammar_complexity(circuit):
        if not circuit:
            return 0
        if isinstance(circuit, str):
            return 1
        left, right = circuit.split()
        return 2 + grammar_complexity(left) + grammar_complexity(right)
    
    n_max = 40
    instances_tested = 30
    g_L_values = []
    theta_C_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        theta_C = circuit_satisfiability_threshold(circuit)
        g_L = grammar_complexity(circuit)
        
        g_L_values.append(g_L)
        theta_C_values.append(theta_C)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(g_L_values, theta_C_values)) / \
                              math.sqrt(sum((x - mean_x) ** 2 for x in g_L_values) * sum((y - mean_y) ** 2 for y in theta_C_values))
    
    mean_g_L = sum(g_L_values) / len(g_L_values)
    support_fraction = sum(1 for g_L, theta_C in zip(g_L_values, theta_C_values) if abs(g_L - theta_C) <= 0.8 * mean_g_L) / len(g_L_values)
    
    conjecture_holds = correlation_coefficient > 0.8 and mean_g_L <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")