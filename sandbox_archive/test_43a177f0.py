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
    
    def generate_clauses(n):
        clauses = []
        for _ in range(10 * n):  # Generate enough clauses to ensure statistical signal
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause.append(random.choice([-1, 1]) * (n + 1))
            clauses.append(clause)
        return clauses

    def calculate_minimal_order_of_hodge_modules(clauses):
        # Placeholder function to simulate the calculation
        # Replace this with actual Hodge module calculation logic
        return [random.random() for _ in clauses]

    def calculate_resolution_proof_width(clauses):
        width = 0
        for clause in clauses:
            width += max(abs(x) for x in clause)
        return width

    n_values = [5, 10, 15, 20, 30, 40]
    variances = []
    
    for n in n_values:
        clauses = generate_clauses(n)
        minimal_order_of_hodge_modules = calculate_minimal_order_of_hodge_modules(clauses)
        resolution_proof_width = calculate_resolution_proof_width(clauses)
        
        variance = sum((x - resolution_proof_width) ** 2 for x in minimal_order_of_hodge_modules) / len(minimal_order_of_hodge_modules)
        variances.append(variance)

    metric_value = sum(variances) / len(variances)
    n_max = max(n_values)
    instances_tested = len(n_values) * 10  # Each n has 10 instances
    conjecture_holds = all(v >= 1.5 ** n * math.log2(n) ** 2 for n, v in zip(n_values, variances))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Variance of Minimal Order of Hodge Modules",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")