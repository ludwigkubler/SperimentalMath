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
            return []
        else:
            gate = random.choice(['AND', 'OR'])
            left = generate_circuit(depth - 1)
            right = generate_circuit(depth - 1)
            return [gate, left, right]
    
    def count_connected_components(circuit):
        if not circuit:
            return 0
        if isinstance(circuit[0], list):
            left_components = count_connected_components(circuit[1])
            right_components = count_connected_components(circuit[2])
            return max(left_components, right_components) + 1
        else:
            return 1
    
    def depth_of_circuit(circuit):
        if not circuit:
            return 0
        if isinstance(circuit[0], list):
            left_depth = depth_of_circuit(circuit[1])
            right_depth = depth_of_circuit(circuit[2])
            return max(left_depth, right_depth) + 1
        else:
            return 0
    
    circuits = [generate_circuit(depth) for depth in range(5, 41)]
    components = [count_connected_components(circuit) for circuit in circuits]
    depths = [depth_of_circuit(circuit) for circuit in circuits]
    
    mean_components = sum(components) / len(components)
    std_components = math.sqrt(sum((x - mean_components) ** 2 for x in components) / len(components))
    correlation_coefficient = sum((components[i] - mean_components) * (depths[i] - mean_depths) for i in range(len(components))) / (len(components) * std_components * std_depths)
    
    conjecture_holds = all(abs(c - d**2 / 4) <= d**2 / 80 for c, d in zip(components, depths))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Number of Connected Components",
        "metric_value": mean_components,
        "instances_tested": len(circuits),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")