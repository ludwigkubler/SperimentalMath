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
    
    def generate_symmetric_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        # Placeholder function to calculate R(f)
        # Replace with actual algorithm or software package
        return len(f) / 2
    
    def symplectic_grassmannian(f):
        # Placeholder function to compute the symplectic Grassmannian
        # Replace with actual implementation using SymPy or other library
        return len(f)  # Simplified for demonstration
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_symmetric_boolean_function(n)
        mol = symplectic_grassmannian(f)
        R_f = communication_complexity_rank(f)
        results.append((n, mol, R_f))
    
    if len(results) < 30:
        return {
            "seed": seed,
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mol_values = [mol for _, mol, _ in results]
    R_f_values = [R_f for _, _, R_f in results]
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def variance(lst, avg):
        return sum((x - avg) ** 2 for x in lst) / len(lst)
    
    mol_avg = mean(mol_values)
    R_f_avg = mean(R_f_values)
    mol_var = variance(mol_values, mol_avg)
    R_f_var = variance(R_f_values, R_f_avg)
    
    covariance = sum((mol_values[i] - mol_avg) * (R_f_values[i] - R_f_avg) for i in range(len(results))) / len(results)
    correlation_coefficient = covariance / math.sqrt(mol_var * R_f_var)
    
    return {
        "seed": seed,
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if abs(correlation_coefficient) >= 0.7 else "correlation_coefficient=0"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")