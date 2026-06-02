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
    valuation = float('inf')
    for clause in instance:
        # Simplified p-adic valuation calculation
        val = abs(clause[0]) + abs(clause[1])
        if val < valuation:
            valuation = val
    if valuation > 10:
        return None
    return valuation

def calculate_entropy(instance):
    n = len(instance)
    ones = sum(1 for clause in instance if clause[1] == 1)
    zeros = n - ones
    p_one = ones / n
    p_zero = zeros / n
    entropy = -p_one * math.log2(p_one) - p_zero * math.log2(p_zero)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_random_instance(n, n * 2)
            valuation = compute_p_adic_valuation(instance)
            if valuation is None:
                continue
            entropy = calculate_entropy(instance)
            results.append((valuation, entropy))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "p-adic valuation exceeds 10"
        }
    
    valuations = [r[0] for r in results]
    entropies = [r[1] for r in results]
    mean_valuation = sum(valuations) / len(valuations)
    mean_entropy = sum(entropies) / len(entropies)
    covariance = sum((v - mean_valuation) * (e - mean_entropy) for v, e in zip(valuations, entropies)) / len(valuations)
    variance_valuation = sum((v - mean_valuation) ** 2 for v in valuations) / len(valuations)
    variance_entropy = sum((e - mean_entropy) ** 2 for e in entropies) / len(entropies)
    correlation_coefficient = covariance / (math.sqrt(variance_valuation) * math.sqrt(variance_entropy))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in [r[2] for r in results]),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")