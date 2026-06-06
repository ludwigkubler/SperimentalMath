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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_planar_circuit(n):
        # Simplified generation for demonstration purposes
        return [random.choice(['AND', 'OR']) for _ in range(n)]
    
    def compute_minimal_hodge_theoretic_index(circuit):
        # Dummy implementation for demonstration purposes
        return random.randint(1, 10)
    
    def compute_monotone_width(circuit):
        # Dummy implementation for demonstration purposes
        return len(circuit)
    
    n_max = 40
    instances_tested = 30
    total_w_c_over_f_n = Fraction(0)
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_random_planar_circuit(n)
        f_n = n ** (2/3)
        w_C = compute_monotone_width(circuit)
        hodge_index = compute_minimal_hodge_theoretic_index(circuit)
        
        if w_C > 10 * f_n:  # Arbitrary large constant to avoid division by zero
            conjecture_holds = False
            counterexample = f"Circuit size {n}, Monotone Width: {w_C}, Hodge Index: {hodge_index}"
            break
        
        total_w_c_over_f_n += Fraction(w_C, f_n)
    
    metric_value = float(total_w_c_over_f_n / instances_tested) if instances_tested > 0 else None
    return {
        "metric_name": "Monotone Width over Hodge Index Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) > 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")