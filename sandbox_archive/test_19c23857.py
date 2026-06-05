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
    
    def generate_circuit(n, w):
        circuit = []
        for _ in range(w):
            gate = random.choice(['AND', 'OR', 'NOT'])
            if gate == 'NOT':
                inputs = [random.randint(0, 1)]
            else:
                inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def construct_quasi_crystal(circuit):
        # Placeholder for actual quasi-crystal construction algorithm
        # For simplicity, we'll just count the number of gates
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    n_max = 0
    
    for n in n_values:
        w = random.randint(1, min(n, 10))  # Width should be at least 1 and <= n
        circuit = generate_circuit(n, w)
        q_c = construct_quasi_crystal(circuit)
        
        if q_c < math.ceil(w ** (2/3)):
            return {
                "metric_name": "Q(C)",
                "metric_value": q_c,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"q_c < w^(2/3) for n={n}, w={w}"
            }
        
        results.append({
            "n": n,
            "w": w,
            "q_c": q_c
        })
        n_max = max(n_max, n)
    
    # Calculate Pearson correlation coefficient
    if len(results) < 30:
        return {
            "metric_name": "Q(C)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances for statistical analysis"
        }
    
    x = [r['w'] ** (2/3) for r in results]
    y = [r['q_c'] for r in results]
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    
    if denominator == 0:
        return {
            "metric_name": "Q(C)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Zero denominator for correlation coefficient"
        }
    
    r = numerator / denominator
    
    return {
        "metric_name": "Q(C)",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": r > 0.1,  # Non-trivially greater than zero
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result['conjecture_holds'] for result in results):
        mean_r = sum(result['metric_value'] for result in results) / len(results)
        std_r = math.sqrt(sum((result['metric_value'] - mean_r) ** 2 for result in results) / len(results))
        support_fraction = len([r for r in results if r['conjecture_holds']]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='<not applicable>' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")