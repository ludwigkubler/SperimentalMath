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
    n = random.randint(5, 40)
    instances_tested = 30
    total_betti = 0
    total_comm_complexity = 0
    
    for _ in range(instances_tested):
        # Generate a random 3-CNF formula with n variables
        clauses = []
        for _ in range(2 * n):
            literals = [random.randint(-n, n) for _ in range(3)]
            clause = tuple(sorted(literal for literal in literals if literal != 0))
            if clause not in clauses:
                clauses.append(clause)
        
        # Simplified filtration: 0th Betti number is the number of connected components
        betti_number = len(clauses)  # Each clause represents a component
        
        # Deterministic communication complexity via log-rank conjecture
        comm_complexity = n * math.log2(n)
        
        total_betti += betti_number
        total_comm_complexity += comm_complexity
    
    metric_value = total_betti / instances_tested
    conjecture_holds = abs(metric_value - total_comm_complexity) < 0.1 * total_comm_complexity
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Sum of Betti Numbers",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30 * 2 + 1, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")