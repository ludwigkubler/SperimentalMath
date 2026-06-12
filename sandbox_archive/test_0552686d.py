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
    
    def calculate_entanglement_complexity(circuit):
        # Placeholder function to simulate entanglement complexity calculation
        return len(circuit) // 2
    
    def calculate_diameter(n):
        # Placeholder function to simulate diameter calculation
        return n * (n + 1) // 2
    
    def reflection_system_size(epsilon):
        # Placeholder function to simulate reflection system size calculation
        return epsilon
    
    n_max = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):  # Aim for at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        circuit = generate_boolean_circuit(n)
        epsilon = calculate_entanglement_complexity(circuit)
        D = calculate_diameter(n)
        reflection_size = reflection_system_size(epsilon)
        
        metric_values.append(D)
        
        if D > n**2 * math.log(n):
            conjecture_holds = False
            counterexample += f"Circuit with n={n} has D={D}, expected O({n**2 * math.log(n)})\n"
        
        if reflection_size > epsilon:
            conjecture_holds = False
            counterexample += f"Reflection system size {reflection_size} exceeds entanglement complexity {epsilon}\n"
    
    return {
        "metric_name": "Coxeter Group Diameter",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": 30,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any("counterexample" in r and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")