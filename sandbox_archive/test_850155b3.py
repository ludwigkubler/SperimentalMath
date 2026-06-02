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
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        instance.append(clause)
    return instance

def compute_p_adic_valuation(instance):
    valuation = float('inf')
    for clause in instance:
        product = 1
        for literal in clause:
            if literal == -1:
                product *= -1
            elif literal == 1:
                continue
            else:
                raise ValueError("Invalid literal in clause")
        valuation = min(valuation, abs(product))
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
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = random.randint(2*n, 3*n)
        instance = generate_random_instance(n, m)
        valuation = compute_p_adic_valuation(instance)
        entropy = calculate_entropy(instance)
        results.append((n, m, valuation, entropy))
    
    n_max = max(n for n, _, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "min_φ(Val(φ)) vs H(φ)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    correlation = 0.0
    for _, _, valuation, entropy in results:
        if valuation > 10:
            continue
        correlation += (valuation - entropy) ** 2
    
    mean_valuation = sum(valuation for _, _, valuation, _ in results) / len(results)
    mean_entropy = sum(entropy for _, _, _, entropy in results) / len(results)
    
    if correlation == 0.0:
        return {
            "metric_name": "min_φ(Val(φ)) vs H(φ)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No correlation found"
        }
    
    return {
        "metric_name": "min_φ(Val(φ)) vs H(φ)",
        "metric_value": mean_valuation * mean_entropy / correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"No correlation found\" first_failing_seed={first_failing_seed}")