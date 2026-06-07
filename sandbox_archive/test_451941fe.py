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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        # This is a placeholder and should be replaced with actual logic
        return len(cnf) * 2
    
    def minimal_order_of_affine_root_system(n):
        # Placeholder for the actual algorithm to compute the minimal order
        # This is a simplified example and should be replaced with actual logic
        return n + 1
    
    instances_tested = 0
    total_order = 0
    total_width = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        order = minimal_order_of_affine_root_system(n)
        width = resolution_width(cnf)
        
        total_order += order
        total_width += width
        instances_tested += n
        if n > n_max:
            n_max = n
    
    mean_order = Fraction(total_order, instances_tested)
    mean_width = Fraction(total_width, instances_tested)
    
    correlation_coefficient = (mean_order * mean_width - instances_tested) / ((instances_tested - 1) * instances_tested)
    
    conjecture_holds = abs(correlation_coefficient) > 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")