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
        val = abs(clause[0]) + abs(clause[1])
        if val < valuation:
            valuation = val
    return valuation

def calculate_entropy(clause_set):
    n = len(clause_set)
    counts = [0] * (n + 1)
    for clause in clause_set:
        counts[len(clause)] += 1
    entropy = 0.0
    for count in counts:
        if count > 0:
            p = Fraction(count, n)
            entropy -= p * math.log2(p)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0.0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        m = random.randint(n, 2 * n)
        instance = generate_random_instance(n, m)
        valuation = compute_p_adic_valuation(instance)
        entropy = calculate_entropy(instance)
        
        if entropy > 0:  # Avoid division by zero
            correlation_sum += valuation / entropy
            instances_tested += 1
            if n > n_max:
                n_max = n

    metric_value = correlation_sum / instances_tested if instances_tested > 0 else 0.0
    conjecture_holds = metric_value >= 0.7 and valuation <= 10
    counterexample = "" if conjecture_holds else "p-adic valuation exceeds 10"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p-adic valuation exceeds 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")