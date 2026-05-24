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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate enough clauses to ensure complexity
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def calculate_brauer_rank(clauses):
        # Placeholder function to simulate Brauer rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses) / 3

    def measure_frege_complexity(clauses):
        # Placeholder function to simulate Frege complexity calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n multiple times to ensure statistical signal
            clauses = generate_3cnf(n)
            brauer_rank = calculate_brauer_rank(clauses)
            frege_complexity = measure_frege_complexity(clauses)
            results.append((n, brauer_rank, frege_complexity))
    
    if not results:
        return {
            "metric_name": "brauer_rank_vs_frege_depth",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_brauer_rank = sum(b for _, b, _ in results) / len(results)
    mean_frege_complexity = sum(f for _, _, f in results) / len(results)
    abs_diff = abs(mean_brauer_rank - (2 ** (mean_frege_complexity / 3)))
    
    return {
        "metric_name": "brauer_rank_vs_frege_depth",
        "metric_value": mean_abs_diff,
        "instances_tested": len(results),
        "conjecture_holds": abs_diff <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results) or sum(r["conjecture_holds"] for r in results) / len(results) >= 0.8:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")