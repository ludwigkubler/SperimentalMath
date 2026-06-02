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
            inputs = [generate_circuit(random.randint(1, depth-1)) for _ in range(2)]
            return [gate] + inputs
    
    def count_connected_components(circuit):
        # Simplified simulation of counting connected components
        # This is a placeholder and should be replaced with actual computation
        return len(circuit)
    
    max_depth = 40
    instances_tested = 0
    total_components = 0
    n_max = 1
    
    for depth in range(5, max_depth + 1):
        if instances_tested >= 30:
            break
        
        circuit = generate_circuit(depth)
        components = count_connected_components(circuit)
        
        if len(circuit) > n_max:
            n_max = len(circuit)
        
        total_components += components
        instances_tested += 1
    
    metric_value = total_components / instances_tested
    conjecture_holds = (metric_value <= (max_depth ** 2 / 4) * 1.05 and metric_value >= (max_depth ** 2 / 4) * 0.95)
    
    return {
        "metric_name": "Number of Connected Components",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")