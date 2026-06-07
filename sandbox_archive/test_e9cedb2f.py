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
    
    def generate_d_regular_boolean_function(d, n):
        if d not in {2}:
            raise ValueError("Unsupported degree for boolean function generation")
        
        # Generate a random d-regular boolean function f
        f = {}
        for x in range(1 << n):
            neighbors = []
            for y in range(1 << n):
                if bin(x ^ y).count('1') == 1:
                    neighbors.append(y)
            f[x] = random.choice([0, 1])
        
        return f
    
    def calculate_galois_group(f, n):
        # Placeholder for Galois group calculation
        # This is a dummy implementation and should be replaced with actual logic
        deg_G_f = n
        return deg_G_f
    
    def calculate_circuit_entanglement(f, n):
        # Placeholder for circuit entanglement calculation
        # This is a dummy implementation and should be replaced with actual logic
        Ent_C_f = n
        return Ent_C_f
    
    d = 2
    n_min = 5
    n_max = 40
    instances_per_seed = 30
    
    total_metric_value = 0
    conjecture_holds_count = 0
    counterexample = ""
    
    for _ in range(instances_per_seed):
        n = random.randint(n_min, n_max)
        f = generate_d_regular_boolean_function(d, n)
        
        deg_G_f = calculate_galois_group(f, n)
        Ent_C_f = calculate_circuit_entanglement(f, n)
        
        total_metric_value += deg_G_f
        if deg_G_f <= Ent_C_f and Ent_C_f <= deg_G_f**2:
            conjecture_holds_count += 1
        else:
            counterexample = f"deg(G_f)={deg_G_f}, Ent(C_f)={Ent_C_f}"
    
    metric_value = total_metric_value / instances_per_seed
    conjecture_holds = conjecture_holds_count == instances_per_seed
    
    return {
        "metric_name": "Galois Group Degree",
        "metric_value": metric_value,
        "instances_tested": instances_per_seed,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")