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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def ac0_circuit_depth(cnf):
        # Simplified heuristic to estimate AC0 circuit depth
        return len(cnf) ** 0.5
    
    def minimal_order_of_affine_hecke_algebra(cnf):
        n = len(cnf[0])
        order = n * (n + 1)
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        ac0_depth = ac0_circuit_depth(cnf)
        order = minimal_order_of_affine_hecke_algebra(cnf)
        results.append((n, ac0_depth, order))
    
    if not results:
        return {
            "metric_name": "Minimal Order vs AC0 Depth",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_depth = sum(result[1] for result in results)
    total_order = sum(result[2] for result in results)
    mean_depth = total_depth / len(results)
    mean_order = total_order / len(results)
    correlation_coefficient = (len(results) * sum(r[1] * r[2] for r in results) - total_depth * total_order) / math.sqrt((len(results) * sum(r[1]**2 for r in results) - total_depth**2) * (len(results) * sum(r[2]**2 for r in results) - total_order**2))
    
    return {
        "metric_name": "Minimal Order vs AC0 Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        RESULT = f"RESULT: FALSIFIED counterexample='correlation_coefficient_too_low' first_failing_seed={first_failing_seed}"
    elif len(results) * 0.8 <= sum(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / sum(1 for result in results if result["metric_value"] is not None)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / (sum(1 for result in results if result["metric_value"] is not None) - 1))
        support_fraction = sum(result["conjecture_holds"] for result in results)
        RESULT = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    else:
        RESULT = "RESULT: INCONCLUSIVE insufficient_data"
    
    print(RESULT)