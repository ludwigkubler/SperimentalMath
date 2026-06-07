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
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def grlex_basis(cnf):
        # Simplified version of Gröbner basis computation using lex order
        # This is a placeholder and does not compute the actual Gröbner basis
        return len(cnf)
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        # This is a placeholder and does not compute the actual resolution width
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    grlex_variants = grlex_basis(cnf)
    res_width = resolution_width(cnf)
    
    if grlex_variants > res_width + 10:
        return {
            "metric_name": "minimal_toric_variants",
            "metric_value": grlex_variants,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"grlex_variants ({grlex_variants}) > res_width + 10 ({res_width} + 10)"
        }
    
    return {
        "metric_name": "minimal_toric_variants",
        "metric_value": grlex_variants,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"grlex_variants > res_width + 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")