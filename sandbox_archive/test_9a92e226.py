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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_deterministic_communication_complexity(f):
    n = int(math.log2(len(f)))
    complexity = 0
    for i in range(n):
        count_0 = f[:2**(i+1)].count(0)
        count_1 = f[:2**(i+1)].count(1)
        if count_0 > 0 and count_1 > 0:
            complexity += 1
    return complexity

def quasi_morphism_rank(f):
    n = int(math.log2(len(f)))
    if n <= 1:
        return 0
    
    def is_quasi_morphism(r, f):
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    if abs(r[i] - r[j]) > 1:
                        return False
        return True
    
    min_rank = n
    for rank in range(1, n + 1):
        for perm in itertools.permutations(range(n), rank):
            r = [0] * n
            for i in range(n):
                if i not in perm:
                    r[i] = f[perm.index(i)]
            if is_quasi_morphism(r, f):
                min_rank = rank
                break
        if min_rank < n:
            break
    
    return min_rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        r = quasi_morphism_rank(f)
        c = compute_deterministic_communication_complexity(f)
        
        if len(results) >= 30:
            break
        
        results.append({
            "n": n,
            "r": r,
            "c": c
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    r_values = [result["r"] for result in results]
    c_values = [result["c"] for result in results]
    
    mean_r = sum(r_values) / len(r_values)
    mean_c = sum(c_values) / len(c_values)
    
    correlation_coefficient = 0
    numerator = sum((r - mean_r) * (c - mean_c) for r, c in zip(r_values, c_values))
    denominator = math.sqrt(sum((r - mean_r)**2 for r in r_values)) * math.sqrt(sum((c - mean_c)**2 for c in c_values))
    
    if denominator == 0:
        correlation_coefficient = None
    else:
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient is not None and abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if correlation_coefficient is not None else "correlation_coefficient_out_of_bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_holds_or_counterexample")