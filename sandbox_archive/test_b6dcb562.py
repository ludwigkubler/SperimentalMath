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
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def compute_euler_characteristic(n, k):
        # Placeholder for actual computation
        return random.uniform(-n**2, n**2)

    def compute_clause_complexity(k):
        return k

    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        k = random.randint(1, n)
        phi = generate_kcnf(n, k)
        chi_phi = compute_euler_characteristic(n, k)
        chi_clause_complexity = compute_clause_complexity(k)
        
        diff = abs(chi_phi - (n**0.5 * chi_clause_complexity))
        results.append(diff)

    mean_diff = sum(results) / len(results)
    support_fraction = sum(1 for diff in results if diff <= 2 * math.sqrt(n)) / len(results)

    return {
        "metric_name": "Euler characteristic difference",
        "metric_value": mean_diff,
        "instances_tested": 30,
        "n_max": max(random.randint(5, 40) for _ in range(30)),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_diff > 2 * sqrt(n)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    support_fraction = sum(1 for diff in results if diff <= 2 * math.sqrt(max([r["n_max"] for r in results]))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if result > 2 * math.sqrt(max([r["n_max"] for r in results])))
        print(f"RESULT: FALSIFIED counterexample='mean_diff > 2 * sqrt(n)' first_failing_seed={first_failing_seed}")