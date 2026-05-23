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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def p_adic_divergence(f, p):
    n = int(math.log2(len(f)))
    count = sum(1 for x in range(2**n) if f[x] != f[0])
    return Fraction(count, 2**n)

def communication_complexity_disjointness(n):
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        D_p_f = p_adic_divergence(f, 2)  # Using base 2 for simplicity
        C_DISJ_n = communication_complexity_disjointness(n)
        
        if D_p_f > 10 or C_DISJ_n > 10:
            return {
                "metric_name": "p-adic divergence vs. communication complexity",
                "metric_value": None,
                "instances_tested": n_values.count(n),
                "conjecture_holds": False,
                "counterexample": f"Metric value exceeded 10 for n={n}"
            }
        
        results.append((D_p_f, C_DISJ_n))
    
    D_p_mean = sum(D_p for D_p, _ in results) / len(results)
    C_DISJ_mean = sum(C_DISJ for _, C_DISJ in results) / len(results)
    
    correlation_coefficient = 0
    if D_p_mean != 0 and C_DISJ_mean != 0:
        numerator = sum((D_p - D_p_mean) * (C_DISJ - C_DISJ_mean) for D_p, C_DISJ in results)
        denominator = math.sqrt(sum((D_p - D_p_mean)**2 for D_p, _ in results)) * math.sqrt(sum((C_DISJ - C_DISJ_mean)**2 for _, C_DISJ in results))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "Correlation coefficient < 0.8"
    
    return {
        "metric_name": "p-adic divergence vs. communication complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [79]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    D_p_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    C_DISJ_values = [r["instances_tested"] for r in results if r["instances_tested"] > 0]
    
    if len(D_p_values) == 0:
        print("RESULT: INCONCLUSIVE no valid data")
    else:
        mean_D_p = sum(D_p_values) / len(D_p_values)
        std_D_p = math.sqrt(sum((x - mean_D_p)**2 for x in D_p_values) / len(D_p_values))
        
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_D_p} std={std_D_p} support_fraction={support_fraction}")
        elif any(r["metric_value"] > 10 for r in results):
            first_failing_seed = next(seed for seed, result in enumerate(results) if result["metric_value"] > 10)
            print(f"RESULT: FALSIFIED counterexample='Metric value exceeded 10' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE support_fraction < 0.8")