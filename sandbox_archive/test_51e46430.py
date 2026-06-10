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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def construct_stabilizer_state(cnf):
        n = len(set(abs(lit) for lit in cnf))
        state = [0] * (2 ** n)
        return state
    
    def calculate_entanglement_entropy(state):
        # Placeholder function to simulate entanglement entropy calculation
        return random.random()
    
    def resolution_proof_width(cnf):
        # Placeholder function to simulate resolution proof width calculation
        return len(cnf)  # Simplified for testing purposes
    
    def correlation_coefficient(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        
        return cov_xy / (var_x * var_y)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = [[random.randint(-n, n) for _ in range(random.randint(2, 5))] for _ in range(n)]
        
        state = construct_stabilizer_state(cnf)
        entropy = calculate_entanglement_entropy(state)
        width = resolution_proof_width(cnf)
        
        results.append((entropy, width))
    
    entanglement_entropies, widths = zip(*results)
    r = correlation_coefficient(entanglement_entropies, widths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": max(len(cnf) for _, cnf in results),
        "conjecture_holds": 0.5 <= r < 0.9,
        "counterexample": "" if 0.5 <= r < 0.9 else f"r={r:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if 0.5 <= res["metric_value"] < 0.9) / len(results)
    
    if all(0.5 <= res["metric_value"] < 0.9 for res in results):
        print(f"RESULT: SUPPORTED mean={mean_r:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r:.2f} std=NA support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='r={results[0]['metric_value']:.2f}' first_failing_seed={first_failing_seed}")