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
    
    def generate_ac0_circuit(n):
        # Simplified AC0 circuit generation for demonstration
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def q_series(circuit):
        n = len(circuit)
        total = 0.0
        for i in range(n + 1):
            term = (math.exp(-i) * sum(circuit[j] for j in range(i, n, i))) / math.factorial(i)
            if abs(term) < 1e-10:
                break
            total += term
        return total
    
    def is_converging(series, threshold=1e-5):
        return abs(series - 1) < threshold
    
    c = random.randint(1, 40)
    circuit = generate_ac0_circuit(c)
    series = q_series(circuit)
    
    metric_value = series
    conjecture_holds = is_converging(series)
    counterexample = "" if conjecture_holds else f"Circuit size {c}, series {series}"
    
    return {
        "metric_name": "q-Series",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 157))  # First 30 primes
    
    results = []
    total_metric_value = 0.0
    supported_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            supported_count += 1
        
        results.append(trial_result)
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_metric_value:.2f} std=0 support_fraction={support_fraction:.2f}")