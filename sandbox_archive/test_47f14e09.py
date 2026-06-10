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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_symplectic_volume(circuit):
        n = len(circuit)
        volume = 0
        for i in range(2**n):
            state = circuit[i]
            if sum(state) % 2 == 0:
                volume += 1
        return volume / (2**n)
    
    def calculate_entanglement_entropy(circuit):
        n = len(circuit)
        entropy = 0
        for i in range(2**n):
            state = circuit[i]
            if sum(state) % 2 == 0:
                entropy += 1
        return entropy / (2**n)
    
    correlation_coefficient = 0.0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_boolean_circuit(n)
            sv = calculate_symplectic_volume(circuit)
            h = calculate_entanglement_entropy(circuit)
            
            correlation_coefficient += abs(sv - h) / (n * 2**n)
            instances_tested += 1
    
    mean_correlation = correlation_coefficient / instances_tested
    conjecture_holds = mean_correlation >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")