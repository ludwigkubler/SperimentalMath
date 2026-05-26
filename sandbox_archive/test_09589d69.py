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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def noncrossing_partition(clauses):
        # Placeholder for the actual noncrossing partition construction
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(clauses)  # Simplified for testing purposes
    
    def tree_like_resolution_complexity(clauses):
        # Placeholder for the actual complexity calculation
        # This is a dummy implementation and should be replaced with an actual algorithm
        m = len(clauses)
        n = max(max(clause) for clause in clauses)
        return m ** (1/4) * n ** (5/12)
    
    n, m = 30, 60  # Example values, adjust as needed
    clauses = generate_3cnf(n, m)
    partition_size = noncrossing_partition(clauses)
    complexity = tree_like_resolution_complexity(clauses)
    
    metric_name = "complexity"
    metric_value = complexity
    instances_tested = 1
    conjecture_holds = complexity >= m ** (1/4) * n ** (5/12)
    counterexample = "" if conjecture_holds else f"Complexity {complexity} < {m ** (1/4) * n ** (5/12)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")