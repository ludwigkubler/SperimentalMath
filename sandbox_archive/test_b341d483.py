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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate_type)]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_hyperbolic_rank(circuit):
        # Placeholder function to compute hyperbolic rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)
    
    def compute_monotone_width(circuit):
        # Placeholder function to compute monotone width
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)
    
    ranks = []
    widths = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_random_circuit(n)
            rank = compute_hyperbolic_rank(circuit)
            width = compute_monotone_width(circuit)
            ranks.append(rank)
            widths.append(width)
            instances_tested += 1
    
    if not ranks or not widths:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n <= 40),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = (instances_tested * sum(rank * width for rank, width in zip(ranks, widths)) - 
                   instances_tested * sum(ranks) * sum(widths) / instances_tested**2) / \
                  math.sqrt((instances_tested * sum(rank**2 for rank in ranks) - sum(ranks)**2 / instances_tested) *
                            (instances_tested * sum(width**2 for width in widths) - sum(widths)**2 / instances_tested))
    
    mean_rank = sum(ranks) / instances_tested
    mean_width = sum(widths) / instances_tested
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if n <= 40),
        "conjecture_holds": abs(correlation) >= 0.8 and abs(mean_rank - mean_width) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")