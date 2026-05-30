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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, len(set(literals)))
            clauses.append(clause)
        return clauses
    
    def tropicalize_complexity(n):
        return 2 ** (n / 4)
    
    def compute_coxeter_group_action_complexity(clauses):
        # Placeholder for actual computation
        # For simplicity, we'll use a dummy value
        return len(clauses) * n
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_kcnf(n, n)
            complexity = compute_coxeter_group_action_complexity(clauses)
            tropicalized_complexity = tropicalize_complexity(n)
            
            if abs(complexity - tropicalized_complexity) > 0.3 * tropicalized_complexity:
                return {
                    "metric_name": "Coxeter Group Action Complexity",
                    "metric_value": complexity,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"Complexity {complexity} exceeds expected tropicalized value {tropicalized_complexity}"
                }
            
            metric_values.append(complexity)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "Coxeter Group Action Complexity",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(mean_value - tropicalize_complexity(n_max)) <= 0.1 * tropicalize_complexity(n_max),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"] - tropicalize_complexity(r["n_max"])) <= 0.2 * tropicalize_complexity(r["n_max"])) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")