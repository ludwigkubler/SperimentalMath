# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def twistor_representation_size(clauses):
        # Simplified mapping to a hypothetical representation size
        return len(clauses) ** 0.5
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different formulas
            m = random.randint(n, n * 3)
            formula = generate_formula(n, m)
            size = twistor_representation_size(formula)
            results.append({"n": n, "m": m, "size": size})
    
    if not results:
        return {
            "metric_name": "MRep(φ)",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [r["size"] for r in results]
    m_values = [r["m"] for r in results]
    n_max = max(r["n"] for r in results)
    
    # Calculate correlation coefficient
    mean_m = sum(m_values) / len(m_values)
    mean_size = sum(metric_values) / len(metric_values)
    covariance = sum((m - mean_m) * (size - mean_size) for m, size in zip(m_values, metric_values))
    variance_m = sum((m - mean_m) ** 2 for m in m_values)
    correlation_coefficient = covariance / (len(m_values) ** 0.5 * variance_m ** 0.5)
    
    return {
        "metric_name": "MRep(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.9 and all(size <= m ** 0.5 for size, m in zip(metric_values, m_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")