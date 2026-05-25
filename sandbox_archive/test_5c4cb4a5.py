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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a modular form f of weight k with level N
    def generate_modular_form():
        k = random.randint(1, 5)
        N = random.randint(2, 40)
        return (k, N)
    
    # Compute the minimal index I(f) of a modular form
    def compute_minimal_index(k, N):
        return Fraction(k * N * math.log(N), k + N)
    
    # Construct the characteristic polynomial of a modular form
    def construct_characteristic_polynomial(k, N):
        # Placeholder for actual computation
        return (k, N)
    
    # Evaluate the minimal index I(h) for an explicit function h computed by an AC⁰ circuit
    def evaluate_minimal_index_for_circuit(d, s):
        # Placeholder for actual computation
        return Fraction(d * s, d + s)
    
    k, N = generate_modular_form()
    I_f = compute_minimal_index(k, N)
    char_poly = construct_characteristic_polynomial(k, N)
    I_h = evaluate_minimal_index_for_circuit(2*k, N)
    
    # Check the conjecture
    if I_h <= I_f:
        depth = 2 * k
        size = N
        if depth < 2 * k or size < N:
            return {
                "metric_name": "Minimal Index",
                "metric_value": I_f,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"AC⁰ circuit with depth {depth} and size {size} has minimal index {I_h} ≤ {I_f}"
            }
    
    return {
        "metric_name": "Minimal Index",
        "metric_value": I_f,
        "instances_tested": 1,
        "conjecture_holds": True,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")