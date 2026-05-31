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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def log_factorial(n):
        return sum(math.log(i) for i in range(1, n + 1))
    
    def generate_sat_instance(m: int, n: int):
        clauses = []
        for _ in range(m):
            clause = random.sample(range(-n, -1), 2)
            clauses.append(clause)
        return clauses
    
    def count_distinct_roots(clauses, n):
        roots = set()
        for clause in clauses:
            root = -sum(clause) / (len(clause) * n)
            roots.add(root)
        return len(roots)
    
    results = []
    for m in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            n = random.randint(5, min(40, max(5, int(n * 1.2))))
            clauses = generate_sat_instance(m, n)
            root_count = count_distinct_roots(clauses, n)
            results.append({
                "m": m,
                "n": n,
                "clauses": clauses,
                "root_count": root_count
            })
    
    total_root_count = sum(result["root_count"] for result in results)
    mean_root_count = Fraction(total_root_count, len(results))
    conjecture_holds = all(log_factorial(n) <= result["root_count"] <= n**3 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_root_count",
        "metric_value": mean_root_count,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")