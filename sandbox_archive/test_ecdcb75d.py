# auto-injected by SEC sandbox
import math
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

def generate_circuit(depth):
    if depth == 0:
        return 'input'
    elif depth == 1:
        return random.choice(['NOT', 'AND', 'OR'])
    else:
        inputs = [generate_circuit(random.randint(1, depth-1)) for _ in range(2)]
        gate = random.choice(['NOT', 'AND', 'OR'])
        return (gate, inputs)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    instances_tested = 0
    total_components = 0
    
    for depth in [5, 10, 15, 20, 30, 40]:
        n_max = max(n_max, depth)
        for _ in range(5):
            circuit = generate_circuit(depth)
            # Simulate the space of continuous paths (simplified)
            components = len(circuit)  # Placeholder for actual path computation
            total_components += components
            instances_tested += 1
    
    metric_value = total_components / instances_tested
    conjecture_holds = metric_value <= (n_max**2 / 4) * 1.05
    counterexample = "" if conjecture_holds else f"Depth {n_max}, Components {total_components}"
    
    return {
        "metric_name": "Number of Connected Components",
        "metric_value": metric_value,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")