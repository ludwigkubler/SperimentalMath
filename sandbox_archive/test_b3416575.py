# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_xor_instance(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def calculate_minimal_order(instance):
        # Simplified representation of minimal order calculation
        return len(set(instance))
    
    def calculate_communication_complexity(instance):
        # XOR communication complexity is n/2 on average
        return len(instance) / 2
    
    rhos = []
    Qs = []
    
    for _ in range(100):  # Ensure at least 30 instances per seed
        instance = generate_xor_instance(random.randint(5, 40))
        rho = calculate_minimal_order(instance)
        Q = calculate_communication_complexity(instance)
        rhos.append(rho)
        Qs.append(Q)
    
    if not rhos or not Qs:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(rhos),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_rho = sum(rhos) / len(rhos)
    mean_Q = sum(Qs) / len(Qs)
    
    covariance = sum((rho - mean_rho) * (Q - mean_Q) for rho, Q in zip(rhos, Qs)) / len(rhos)
    std_rho = math.sqrt(sum((rho - mean_rho)**2 for rho in rhos) / len(rhos))
    std_Q = math.sqrt(sum((Q - mean_Q)**2 for Q in Qs) / len(Qs))
    
    if std_rho == 0 or std_Q == 0:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(rhos),
            "conjecture_holds": False,
            "counterexample": "zero_std"
        }
    
    correlation_coefficient = covariance / (std_rho * std_Q)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(rhos),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    default_seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    seeds = list(map(int, sys.argv[1:])) or default_seeds
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        mean_value = None
        std_value = None
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")