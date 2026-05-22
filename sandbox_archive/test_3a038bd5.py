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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def p_adic_derivative(f):
        n = len(f)
        if n == 1:
            return [0]
        derivative = []
        for i in range(1, n):
            derivative.append((f[i] - f[0]) % 2)
        return derivative
    
    def circuit_complexity(f):
        # Simplified stub function to represent circuit complexity
        n = len(f)
        return n * (n + 1) // 2
    
    instances_tested = 40
    ranks = []
    circuit_sizes = []
    
    for _ in range(instances_tested):
        f = generate_boolean_function(5)  # Using a fixed size for simplicity
        rank = len(p_adic_derivative(f))
        circuit_size = circuit_complexity(f)
        ranks.append(rank)
        circuit_sizes.append(circuit_size)
    
    if not ranks or not circuit_sizes:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_circuit_size = sum(circuit_sizes) / len(circuit_sizes)
    
    if len(ranks) < 2:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    numerator = sum((r - mean_rank) * (c - mean_circuit_size) for r, c in zip(ranks, circuit_sizes))
    denominator = math.sqrt(sum((r - mean_rank)**2 for r in ranks)) * math.sqrt(sum((c - mean_circuit_size)**2 for c in circuit_sizes))
    
    if denominator == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        counterexample_desc = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")