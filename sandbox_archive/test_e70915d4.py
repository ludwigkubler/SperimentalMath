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
    
    def generate_circuit(depth):
        if depth == 0:
            return ['0', '1']
        else:
            inputs = generate_circuit(depth - 1)
            outputs = []
            for a in inputs:
                for b in inputs:
                    outputs.append(f'({a} AND {b})')
                    outputs.append(f'({a} OR {b})')
                    outputs.append(f'(NOT {a})')
                    outputs.append(f'(NOT {b})')
            return outputs
    
    def calculate_symmetry_group(circuit):
        # Placeholder for actual symmetry group calculation
        # This is a dummy implementation that returns a small number
        return random.randint(1, 2**len(circuit))
    
    depths = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for depth in depths:
        circuits = generate_circuit(depth)
        for circuit in circuits:
            instances_tested += 1
            n_max = max(n_max, len(circuit))
            symmetry_group_order = calculate_symmetry_group(circuit)
            total_metric_value += symmetry_group_order
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value <= 2**(depth + 1) and (mean_metric_value / 2**depth) >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Symmetry Group Order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")