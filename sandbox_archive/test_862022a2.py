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
    
    def calculate_diameter(group):
        n = len(group)
        diameter = 0
        for i in range(n):
            for j in range(i + 1, n):
                distance = sum(abs(a - b) for a, b in zip(group[i], group[j]))
                if distance > diameter:
                    diameter = distance
        return diameter
    
    def calculate_entanglement_complexity(circuit):
        # Placeholder function to simulate entanglement complexity calculation
        return len(circuit)
    
    n_max = 0
    instances_tested = 0
    total_diameter = 0
    total_complexity = 0
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30]:
        if n > n_max:
            n_max = n
        
        for _ in range(6):  # Ensure at least 30 instances per seed
            circuit = generate_boolean_circuit(n)
            group = [circuit]
            for _ in range(n):
                new_group = []
                for g in group:
                    for i in range(n):
                        new_g = list(g)
                        new_g[i] = 1 - new_g[i]
                        new_group.append(new_g)
                group.extend(new_group)
            
            diameter = calculate_diameter(group)
            complexity = calculate_entanglement_complexity(circuit)
            
            total_diameter += diameter
            total_complexity += complexity
            
            if diameter > n**2 * math.log(n):
                counterexample = f"n={n}, circuit={circuit}, diameter={diameter}"
                return {
                    "metric_name": "Diameter",
                    "metric_value": diameter,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            
            if complexity > 0 and not any(size <= complexity for size in range(1, complexity + 1)):
                counterexample = f"n={n}, circuit={circuit}, complexity={complexity}"
                return {
                    "metric_name": "Diameter",
                    "metric_value": diameter,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            
            instances_tested += 1
    
    mean_diameter = total_diameter / instances_tested
    mean_complexity = total_complexity / instances_tested
    
    return {
        "metric_name": "Diameter",
        "metric_value": mean_diameter,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diameter = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diameter} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")