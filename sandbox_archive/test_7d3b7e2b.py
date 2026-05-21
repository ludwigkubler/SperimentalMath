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

def generate_monotone_circuit(n, k):
    if n < k:
        return None  # Invalid circuit for given n and k
    
    circuit = []
    for _ in range(k):
        layer = [random.choice([0, 1]) for _ in range(n)]
        circuit.append(layer)
    
    return circuit

def compute_cross_sectional_area(circuit):
    if not circuit:
        return 0
    
    n = len(circuit[0])
    area = 0
    for i in range(1 << n):
        hyperplane = [bool(i & (1 << j)) for j in range(n)]
        count = sum(1 for layer in circuit if all(layer[j] == hyperplane[j] for j in range(n)))
        area += count
    
    return area

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = min(n, 4)  # Ensure k is at most n
        circuit = generate_monotone_circuit(n, k)
        
        if not circuit:
            return {
                "metric_name": "cross_sectional_area",
                "metric_value": 0,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": "invalid_circuit"
            }
        
        area = compute_cross_sectional_area(circuit)
        results.append(area)
    
    mean_area = sum(results) / len(results)
    conjecture_holds = all(area >= n**(k/2) for area, k in zip(results, n_values))
    
    return {
        "metric_name": "cross_sectional_area",
        "metric_value": mean_area,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "area_too_small"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result["metric_value"])
    
    if len(results) == len(seeds):
        mean_area = sum(results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_area} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = seeds[results.index(min(results))]
        result = f"RESULT: FALSIFIED counterexample=\"area_too_small\" first_failing_seed={first_failing_seed}"
    
    print(result)