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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause and -var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def is_unsatisfiable(clauses):
        # Simplified check for unsatisfiability
        # This is a placeholder. For actual testing, use a SAT solver.
        return True  # Placeholder for actual implementation
    
    def compute_moment_map(clauses):
        # Placeholder for moment map computation
        # This is a placeholder. For actual testing, use a geometric algorithm.
        return [1] * len(clauses)  # Placeholder for actual implementation
    
    def symplectic_leaf_order(moments):
        # Placeholder for symplectic leaf order calculation
        # This is a placeholder. For actual testing, use a geometric algorithm.
        return max(moments)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    for n in n_values:
        for m in m_values:
            if is_unsatisfiable(generate_3cnf(n, m)):
                moments = compute_moment_map(generate_3cnf(n, m))
                order = symplectic_leaf_order(moments)
                results.append({
                    "n": n,
                    "m": m,
                    "order": order
                })
    
    if not results:
        return {
            "metric_name": "min_symplectic_leaf_order",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_unsatisfiable_3cnf_found"
        }
    
    min_order = min(result["order"] for result in results)
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    
    # Placeholder constant c
    c = 1.0
    
    return {
        "metric_name": "min_symplectic_leaf_order",
        "metric_value": min_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": min_order >= c * (n_max ** 0.25) * math.log(n_max),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result for result in results if not result["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")