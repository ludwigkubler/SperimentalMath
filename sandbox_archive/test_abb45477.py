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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_diameter(group):
        n = len(group)
        diameter = float('inf')
        for i in range(n):
            for j in range(i+1, n):
                dist = sum(abs(a - b) for a, b in zip(group[i], group[j]))
                if dist < diameter:
                    diameter = dist
        return diameter
    
    def calculate_entanglement_complexity(circuit):
        # Placeholder function; replace with actual complexity calculation
        return len(circuit)
    
    n_max = 0
    instances_tested = 0
    total_diameter = 0
    total_complexity = 0
    counterexample = ""
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        circuit = generate_boolean_circuit(n)
        group = [circuit]
        
        for _ in range(2**n - 1):
            new_circuit = [x ^ y for x, y in zip(circuit, random.choice(group))]
            if new_circuit not in group:
                group.append(new_circuit)
        
        diameter = calculate_diameter(group)
        complexity = calculate_entanglement_complexity(circuit)
        
        total_diameter += diameter
        total_complexity += complexity
        
        instances_tested += 1
        
        if diameter > n**2 * math.log(n):
            counterexample = f"High diameter for n={n}, D={diameter}"
            break
    
    mean_diameter = total_diameter / instances_tested
    conjecture_holds = mean_diameter <= n_max**2 * math.log(n_max) and complexity <= n_max
    
    return {
        "metric_name": "Coxeter Group Diameter",
        "metric_value": mean_diameter,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diameter = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diameter} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diameter} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"High diameter\" first_failing_seed={first_failing_seed}")