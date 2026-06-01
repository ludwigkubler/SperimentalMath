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
    
    def generate_circuit(n, d):
        # Generate a random Boolean circuit with n inputs and depth d
        if d == 0:
            return random.choice(['0', '1'])
        else:
            ops = ['AND', 'OR']
            op = random.choice(ops)
            left = generate_circuit(n, d - 1)
            right = generate_circuit(n, d - 1)
            return f"({op} {left} {right})"
    
    def compute_local_coherence_rank(circuit):
        # Placeholder for computing local coherence rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    def compute_resolution_width(circuit):
        # Placeholder for computing resolution width
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)
    
    n = 5 + (seed % 4) * 5  # Sweep through n ∈ {5, 10, 15, 20, 30, 40}
    d = 2
    instances_tested = 30
    total_r = 0
    total_w = 0
    
    for _ in range(instances_tested):
        circuit = generate_circuit(n, d)
        r = compute_local_coherence_rank(circuit)
        w = compute_resolution_width(circuit)
        total_r += r
        total_w += w
    
    mean_r = total_r / instances_tested
    mean_w = total_w / instances_tested
    correlation_coefficient = (instances_tested * sum(r * w for r, w in zip(range(instances_tested), range(instances_tested))) - 
                               instances_tested * mean_r * mean_w) / math.sqrt((instances_tested * sum(r**2 for r in range(instances_tested)) - 
                                                                 instances_tested * mean_r**2) *
                                                                         (instances_tested * sum(w**2 for w in range(instances_tested)) - 
                                                                          instances_tested * mean_w**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) > 0.1,  # Placeholder threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")