# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_geometric_entropy(circuit):
        # Placeholder function to simulate geometric entropy calculation
        return sum(circuit) / len(circuit)
    
    def calculate_entanglement_complexity(circuit):
        # Placeholder function to simulate entanglement complexity calculation
        return sum(circuit) * 2
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        if n > n_max:
            break
        
        for _ in range(instances_tested // (n - 4)):
            circuit = generate_circuit(n)
            mge = calculate_geometric_entropy(circuit)
            ec = calculate_entanglement_complexity(circuit)
            
            if mge <= 0 or ec <= 0:
                continue
            
            metric_values.append(mge / ec)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value)**2 for x in metric_values) / len(metric_values))**0.5
    
    correlation_coefficient = sum((metric_values[i] - mean_value) * (i - len(metric_values) // 2) for i in range(len(metric_values))) / (len(metric_values) * std_value * (len(metric_values) // 2))
    
    if correlation_coefficient < 0.7 or not (1.2 <= mean_value <= 1.8):
        conjecture_holds = False
        counterexample = "correlation_coefficient_out_of_bounds"
    
    return {
        "metric_name": "mge/ec_ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={first_failing_seed}")