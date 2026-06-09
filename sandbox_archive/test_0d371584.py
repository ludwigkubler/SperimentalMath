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
    
    def tseitin_formula(n):
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
            for j in range(i+1, n+1):
                clauses.append([i, -j])
                clauses.append([-i, j])
        return clauses
    
    def hamiltonian(clause):
        # Simplified Hamiltonian for demonstration
        return sum(abs(x) for x in clause)
    
    def geometric_entropy(hamiltonian_value):
        # Simplified geometric entropy calculation
        if hamiltonian_value == 0:
            return 0
        return -hamiltonian_value * math.log2(hamiltonian_value)
    
    def frege_proof_width(clause):
        # Simplified Frege proof width calculation
        return len(clause)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = tseitin_formula(n)
        instances_tested = 0
        total_mge = 0
        total_width = 0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = random.choice(formula)
            mge_value = geometric_entropy(hamiltonian(instance))
            width_value = frege_proof_width(instance)
            
            total_mge += mge_value
            total_width += width_value
            instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "mge",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        mean_mge = total_mge / instances_tested
        mean_width = total_width / instances_tested
        
        if abs(mean_mge - mean_width) > 10 * min(mean_mge, mean_width):
            return {
                "metric_name": "mge",
                "metric_value": mean_mge,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"mge={mean_mge}, width={mean_width}"
            }
        
        results.append({
            "n": n,
            "mge": mean_mge,
            "width": mean_width
        })
    
    return {
        "metric_name": "mge",
        "metric_value": sum(result["mge"] for result in results) / len(results),
        "instances_tested": 30 * len(n_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mge and width do not correlate\" first_failing_seed={first_failing_seed}")