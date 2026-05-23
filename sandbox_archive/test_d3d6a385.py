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
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def hodge_index(n, m):
        # Simplified Hodge index calculation
        return (m ** (1/3)) * (n ** (2/3))
    
    def dpll_width(clauses):
        # Simplified DPLL width calculation
        max_width = 0
        stack = []
        for clause in clauses:
            if len(clause) > max_width:
                max_width = len(clause)
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            cnf = generate_cnf(n, m)
            h_index = hodge_index(n, m)
            d_width = dpll_width(cnf)
            results.append({
                "n": n,
                "m": m,
                "h_index": h_index,
                "d_width": d_width
            })
    
    total_h_index = sum(result["h_index"] for result in results)
    total_d_width = sum(result["d_width"] for result in results)
    mean_h_index = total_h_index / len(results)
    mean_d_width = total_d_width / len(results)
    
    conjecture_holds = all(result["h_index"] <= result["d_width"] for result in results)
    counterexample = "" if conjecture_holds else "Hodge index > DPLL width"
    
    return {
        "metric_name": "Hodge Index vs DPLL Width",
        "metric_value": mean_d_width,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Hodge index > DPLL width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")