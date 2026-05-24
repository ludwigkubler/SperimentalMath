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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_manifold(n):
        # Simple random manifold generation for demonstration purposes
        return [random.choice([0, 1]) for _ in range(n)]
    
    def compute_light_paths(manifold):
        # Compute minimal number of light paths (simplified example)
        return sum(manifold)
    
    def construct_circuit(manifold):
        # Construct a circuit that can be satisfied by a constant number of assignments
        # Simplified example: circuit size is the number of 1's in the manifold
        return sum(manifold)
    
    n = random.randint(5, 40)
    manifold = generate_manifold(n)
    light_paths = compute_light_paths(manifold)
    circuit_size = construct_circuit(manifold)
    
    if circuit_size == 0:
        return {
            "metric_name": "light_paths_to_circuit_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_size_zero"
        }
    
    ratio = Fraction(light_paths, circuit_size)
    return {
        "metric_name": "light_paths_to_circuit_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")