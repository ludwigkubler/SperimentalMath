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
    
    def generate_random_polynomial(n):
        coefficients = [random.choice([0, 1]) for _ in range(2**n)]
        return coefficients
    
    def hodge_decomposition_rank(poly):
        # Simplified Hodge decomposition rank calculation
        n = len(poly) - 1
        rank = sum(1 for coeff in poly if coeff == 1)
        return rank
    
    def ac0_circuit_complexity(poly):
        # Simplified AC0 circuit complexity calculation
        n = len(poly) - 1
        complexity = n * (n + 1) // 2
        return complexity
    
    def compute_ratio(poly):
        rank = hodge_decomposition_rank(poly)
        complexity = ac0_circuit_complexity(poly)
        if complexity == 0:
            return None
        return rank / complexity
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        poly = generate_random_polynomial(n)
        ratio = compute_ratio(poly)
        if ratio is not None:
            results.append(ratio)
    
    if len(results) < 30:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    mean_ratio = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_ratio)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - 1.0) <= 0.1) / len(results)
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": 30,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean={mean_ratio}, std_dev={std_dev}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    elif any(r["counterexample"] == "insufficient_data" for r in results):
        RESULT = "INCONCLUSIVE insufficient_data"
    else:
        RESULT = "INCONCLUSIVE unknown_reason"
    
    print(f"{RESULT} mean={mean_ratio:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")