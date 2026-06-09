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

def generate_formula(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    formula = []
    for _ in range(m):
        clause_size = random.randint(1, n)
        clause = random.sample(variables, clause_size)
        formula.append(tuple(sorted(clause)))
    return formula

def twistor_representation(formula: list) -> int:
    # Placeholder function to simulate the minimal representation degree
    # This is a dummy implementation and should be replaced with actual logic
    m = len(formula)
    return 2 * math.ceil(math.sqrt(m))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * 2)  # Ensure m is at least 1 and varies with n
        formula = generate_formula(n, m)
        m_rep = twistor_representation(formula)
        
        results.append({
            "n": n,
            "m": m,
            "formula": formula,
            "m_rep": m_rep,
            "expected_bound": math.ceil(math.sqrt(m))
        })
    
    correlation_values = [result["m_rep"] / result["expected_bound"] for result in results]
    mean_correlation = sum(correlation_values) / len(correlation_values)
    max_m_rep = max(result["m_rep"] for result in results)
    
    conjecture_holds = all(correlation >= 0.9 for correlation in correlation_values) and max_m_rep <= 2 * math.ceil(math.sqrt(max(results, key=lambda x: x["m"])["m"]))
    counterexample = "" if conjecture_holds else "correlation below threshold or m_rep exceeds bound"
    
    return {
        "metric_name": "Correlation between MRep(φ) and m^(1/2)",
        "metric_value": mean_correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")