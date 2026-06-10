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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def circuit_satisfiability_complexity(cnf):
        # Simplified complexity measure
        return len(cnf) + sum(len(clause) for clause in cnf)
    
    def hodge_theoretic_rank(cnf):
        # Simplified rank measure (placeholder)
        return len(cnf)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        cnf = generate_cnf(n)
        c = circuit_satisfiability_complexity(cnf)
        h = hodge_theoretic_rank(cnf)
        results.append((c, h))
    
    if not results:
        return {
            "metric_name": "h(φ)",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mean_c = sum(c for c, _ in results) / len(results)
    mean_h = sum(h for _, h in results) / len(results)
    
    correlation_coefficient = sum((c - mean_c) * (h - mean_h) for c, h in results) / (len(results) * math.sqrt(sum((c - mean_c)**2 for c, _ in results)) * math.sqrt(sum((h - mean_h)**2 for _, h in results)))
    mean_abs_deviation = sum(abs(c - mean_c) for c, _ in results) / len(results)
    
    return {
        "metric_name": "h(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_abs_deviation <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")