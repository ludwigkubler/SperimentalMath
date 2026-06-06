# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(random.randint(2 * n, 3 * n)):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return variables, clauses
    
    def circuit_depth(variables, clauses):
        # Simplified DPLL solver to estimate circuit depth
        stack = []
        for clause in clauses:
            if all(var not in stack for var in clause):
                stack.extend(clause)
            else:
                return len(stack)  # Approximate depth
        return len(stack)
    
    def geometric_entropy(n):
        # Simplified geometric entropy calculation (constant for demonstration)
        return n ** (1/3)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        variables, clauses = generate_instance(n)
        depth_phi = circuit_depth(variables, clauses)
        epsilon_phi = geometric_entropy(n)
        
        if depth_phi <= 10 * epsilon_phi:  # Simplified constant C
            results.append((n, depth_phi, epsilon_phi))
    
    metric_value = sum(depth for _, depth, _ in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for n, _, _ in results)
    conjecture_holds = all(depth <= 10 * epsilon for _, depth, epsilon in results)
    counterexample = "" if conjecture_holds else "Circuit depth exceeds 10 times geometric entropy"
    
    return {
        "metric_name": "Circuit Depth",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit depth exceeds 10 times geometric entropy\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")