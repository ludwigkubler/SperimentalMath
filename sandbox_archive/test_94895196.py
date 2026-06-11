# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n, d):
        if n == 1:
            return [0]
        circuit = []
        for _ in range(d):
            layer = random.sample(range(1, n), n-1)
            circuit.extend(layer)
        return circuit
    
    def entanglement_complexity(circuit):
        return len(set(circuit))
    
    def fourier_multiplier(circuit):
        n = len(circuit) + 1
        A = [[0] * n for _ in range(n)]
        for i in range(1, n):
            for j in range(1, n):
                if i != j:
                    A[i][j] = (math.cos(2 * math.pi * i * j / n) - 1) / (i * j)
        return A
    
    def matrix_norm(A):
        max_norm = 0
        for row in A:
            norm = sum(abs(x) for x in row)
            if norm > max_norm:
                max_norm = norm
        return max_norm
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n, random.randint(2, min(4, n-1)))
        E_C = entanglement_complexity(circuit)
        M_C = fourier_multiplier(circuit)
        norm_M_C = matrix_norm(M_C)
        
        results.append({
            "n": n,
            "E_C": E_C,
            "norm_M_C": norm_M_C
        })
    
    if not results:
        return {
            "metric_name": "norm_M_C",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    max_norm = max(result["norm_M_C"] for result in results)
    avg_norm = sum(result["norm_M_C"] for result in results) / len(results)
    
    c = 1.0  # Placeholder constant
    conjecture_holds = all(max_norm <= c * result["E_C"] ** 2 for result in results)
    
    return {
        "metric_name": "norm_M_C",
        "metric_value": avg_norm,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_norm={max_norm} > c * E_C^2 for some circuit"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_norm > c * E_C^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")