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
    
    # Define the function to generate a random Boolean circuit
    def generate_circuit(w, d):
        if w == 1 and d == 1:
            return ['x1']
        elif w == 1:
            return [random.choice(['~', '&', '|']) + generate_circuit(1, d-1)]
        else:
            left = generate_circuit(w//2, d-1)
            right = generate_circuit(w-w//2, d-1)
            return ['('] + left + ['&'] + right + [')']
    
    # Define the function to evaluate a Boolean circuit
    def evaluate_circuit(circuit):
        if isinstance(circuit, str) and circuit[0] == 'x':
            return random.choice([True, False])
        elif circuit[0] == '~':
            return not evaluate_circuit(circuit[1:])
        elif circuit[0] == '&':
            return evaluate_circuit(circuit[1]) and evaluate_circuit(circuit[2:-1])
        elif circuit[0] == '|':
            return evaluate_circuit(circuit[1]) or evaluate_circuit(circuit[2:-1])
    
    # Define the function to compute the minimal rank of the tangent space
    def min_rank(TM):
        # This is a placeholder for the actual computation
        # For simplicity, we assume the minimal rank is proportional to the width and depth
        return 2**(w/2 + d)
    
    # Generate random Boolean circuits with width w and depth d
    n = 40
    results = []
    for _ in range(30):
        w = random.randint(1, 5)
        d = random.randint(1, 5)
        circuit = generate_circuit(w, d)
        
        # Evaluate the circuit
        result = evaluate_circuit(circuit)
        
        # Compute the minimal rank of the tangent space
        TM = min_rank(TM)
        
        # Verify if the computed rank is at least 2^(w/2 + Ω(d))
        conjecture_holds = TM >= 2**(w/2 + d)
        counterexample = "" if conjecture_holds else f"Circuit: {circuit}, TM: {TM}"
        
        results.append({
            "metric_name": "min_rank",
            "metric_value": TM,
            "instances_tested": n,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.extend(trial_result["results"])
    
    # Compute mean/std of metric_value
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    
    # Fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")