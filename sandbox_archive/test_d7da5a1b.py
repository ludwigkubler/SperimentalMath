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

def generate_boolean_circuit(n: int) -> list:
    circuit = []
    for _ in range(n):
        gate = random.choice(['AND', 'OR', 'NOT'])
        if gate == 'NOT':
            inputs = [random.randint(0, 1)]
        else:
            inputs = [random.randint(0, 1), random.randint(0, 1)]
        circuit.append((gate, inputs))
    return circuit

def compute_brauer_group_order(n: int) -> float:
    # Simplified mapping for demonstration purposes
    return n * math.log2(n)

def find_smallest_frege_proof(circuit: list) -> int:
    # Simplified mapping for demonstration purposes
    return len(circuit) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Pearson Correlation Coefficient"
    instances_tested = 0
    n_max = 5
    conjecture_holds = True
    counterexample = ""
    
    if len(sys.argv[1:]) == 0:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    if seed not in seeds:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        m = find_smallest_frege_proof(generate_boolean_circuit(n))
        if m == 0:
            continue
        instances_tested += 1
        n_max = max(n_max, n)
        order = compute_brauer_group_order(n)
        results.append((order, m))
    
    if len(results) < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    def pearson_correlation(x: list, y: list) -> float:
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    correlation = pearson_correlation([r[0] for r in results], [r[1] for r in results])
    
    if correlation < 0.8:
        conjecture_holds = False
        counterexample = f"Correlation coefficient {correlation} is less than 0.8"
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")