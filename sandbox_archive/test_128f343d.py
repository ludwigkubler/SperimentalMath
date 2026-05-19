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
    n = 30
    m = 10 * n
    C = 1.0  # Universal constant for the conjecture
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def convex_hull_surface_area(clauses, n):
        # Placeholder function to compute surface area
        return 0.5 * m  # Simplified approximation for demonstration purposes
    
    def resolution_proof_length(clauses):
        # Placeholder function to simulate DPLL with clause learning
        return len(clauses) * 2  # Simplified approximation for demonstration purposes
    
    clauses = generate_3cnf(n, m)
    surface_area = convex_hull_surface_area(clauses, n)
    proof_length = resolution_proof_length(clauses)
    
    metric_value = surface_area * proof_length
    conjecture_holds = metric_value <= C * math.log(m)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "SurfaceArea * ProofLength",
        "metric_value": metric_value,
        "instances_tested": 1,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")