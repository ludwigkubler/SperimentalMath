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
    
    def generate_polynomial_system(n, k_n):
        poly_system = []
        for _ in range(k_n):
            coeffs = [random.choice([-1, 1]) * sum(random.choices([x**i for i in range(n+1)], k=2)) for x in range(1, n+1)]
            poly_system.append(coeffs)
        return poly_system
    
    def calculate_k_complexity(poly_system):
        # Placeholder function to simulate K-complexity calculation
        return len(poly_system) * n  # Simplified for testing purposes
    
    def calculate_symplectic_rank(poly_system):
        # Placeholder function to simulate symplectic rank calculation
        return sum(len(poly) for poly in poly_system)
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k_n = random.randint(1, min(n, 10))  # Ensure K-complexity is at least 1
        poly_system = generate_polynomial_system(n, k_n)
        k_complexity = calculate_k_complexity(poly_system)
        symplectic_rank = calculate_symplectic_rank(poly_system)
        
        if k_complexity == 0:
            continue
        
        ratio = Fraction(symplectic_rank, log2(k_complexity) ** 2).limit_denominator()
        results.append((n, k_n, symplectic_rank, k_complexity, ratio))
    
    if not results:
        return {
            "metric_name": "symplectic_rank_ratio",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_ratio = sum(result[4] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result[4] - mean_ratio) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "symplectic_rank_ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "conjecture_holds": all(result[4] <= Fraction(1, 10) for result in results),  # Placeholder constant c
        "counterexample": "" if all(result[4] <= Fraction(1, 10) for result in results) else "Ratio exceeded"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result['metric_value'] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result['metric_value'] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")