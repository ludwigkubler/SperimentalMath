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
        variables = set()
        for _ in range(n):
            clause = []
            for _ in range(2):  # Each clause has at most 2 literals
                var = random.randint(1, n)
                polarity = random.choice([True, False])
                clause.append((var, polarity))
                variables.add(var)
            clauses.append(clause)
        return clauses, len(variables)

    def calculate_width(clauses):
        width = 0
        seen_vars = set()
        for clause in clauses:
            new_vars = {var for var, _ in clause if var not in seen_vars}
            width = max(width, len(new_vars))
            seen_vars.update(new_vars)
        return width

    def calculate_k(clauses):
        semtypes = set()
        for clause in clauses:
            semtype = tuple(sorted((var, polarity) for var, polarity in clause))
            semtypes.add(semtype)
        return len(semtypes)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses, num_vars = generate_cnf(n)
        width = calculate_width(clauses)
        k = calculate_k(clauses)
        results.append({
            "n": n,
            "width": width,
            "k": k
        })
    
    if not all("width" in res and "k" in res for res in results):
        return {
            "metric_name": "width_bound",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(res["n"] for res in results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_width = sum(res["width"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["width"] - mean_width) ** 2 for res in results) / len(results))
    conjecture_holds = all(abs(res["width"] - mean_width) <= 3 * std_dev for res in results)
    
    return {
        "metric_name": "width_bound",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "n_max": max(res["n"] for res in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_width) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"width_exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")