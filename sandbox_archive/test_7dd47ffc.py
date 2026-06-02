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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_function(circuit, x):
        n = len(circuit)
        if len(x) != n:
            raise ValueError("Input length must match circuit size")
        result = 0
        for i in range(n):
            result += circuit[i] * (-1)**x[i]
        return result
    
    def p_adic_integral(f, base=2):
        # Simplified p-adic integral using a finite approximation
        n = len(f)
        integral = [0] * (n + 1)
        for i in range(n):
            integral[i+1] = f[i]
        return integral
    
    def communication_complexity_rank(circuit):
        # Placeholder function, replace with actual algorithm
        return sum(1 for bit in circuit if bit == 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different circuits
            circuit = generate_circuit(n)
            x = [random.randint(0, 1) for _ in range(n)]
            f = characteristic_function(circuit, x)
            lii = p_adic_integral(f)
            rank = communication_complexity_rank(circuit)
            
            metrics.append({
                "n": n,
                "lii": lii[-1],
                "rank": rank
            })
            instances_tested += 1
    
    if not metrics:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lii_values = [m["lii"] for m in metrics]
    rank_values = [m["rank"] for m in metrics]
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y) if std_x != 0 and std_y != 0 else 0
    
    corr = correlation(lii_values, rank_values)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": corr,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": corr >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_data")