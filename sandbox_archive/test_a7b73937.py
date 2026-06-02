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

def generate_random_instance(n, m):
    instance = []
    for _ in range(m):
        clause = [random.randint(1, n), random.choice([-1, 1])]
        instance.append(clause)
    return instance

def compute_p_adic_valuation(instance):
    p = 2
    valuation = float('inf')
    for clause in instance:
        val = abs(clause[0] * clause[1])
        if val % p == 0:
            valuation = min(valuation, math.log2(val))
    return valuation

def calculate_entropy(clause_set):
    n = len(clause_set)
    counts = [sum(1 for c in clause_set if c[1] == i) for i in [-1, 1]]
    probabilities = [c / n for c in counts]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_name = "correlation_coefficient"
    instances_tested = 0
    n_max = 0
    correlation_sum = 0.0
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2*n)
            instance = generate_random_instance(n, m)
            valuation = compute_p_adic_valuation(instance)
            entropy = calculate_entropy(instance)
            instances_tested += 1
            n_max = max(n_max, n)
            
            if valuation > 10:
                counterexample = "p-adic valuation exceeds 10"
                return {
                    "metric_name": metric_name,
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            
            correlation_sum += valuation / entropy
    
    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient instances tested"
        }
    
    average_correlation = correlation_sum / instances_tested
    return {
        "metric_name": metric_name,
        "metric_value": average_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": average_correlation >= 0.7,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")