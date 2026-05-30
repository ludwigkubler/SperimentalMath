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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_euler_characteristic(n, m):
        # Euler characteristic of a graph with n vertices and m edges
        return n - m + 1
    
    def compute_clause_complexity(clauses):
        return len(clauses)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        k = random.randint(1, n * (n - 1) // 2)
        clauses = generate_k_cnf(n, k)
        
        m = len(clauses)
        chi_phi = compute_clause_complexity(clauses)
        chi_C_phi = compute_euler_characteristic(n, m)
        
        diff = abs(chi_C_phi - math.sqrt(n) * chi_phi)
        results.append(diff)
    
    mean_diff = sum(results) / len(results)
    support_fraction = sum(1 for diff in results if diff <= 2 * math.sqrt(n)) / len(results)
    
    return {
        "metric_name": "Euler characteristic difference",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": max(random.randint(5, 40) for _ in range(30)),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "mean_diff > 2 * sqrt(n)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
    results = [run_trial(seed)["metric_value"] for seed in seeds]
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for diff in results if diff <= 2 * math.sqrt(n)) / len(results)
    
    if all(diff <= 2 * math.sqrt(n) for n, diff in zip([max(random.randint(5, 40) for _ in range(30))] * len(seeds), results)):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(diff > 2 * math.sqrt(n) for n, diff in zip([max(random.randint(5, 40) for _ in range(30))] * len(seeds), results)):
        first_failing_seed = seeds[next(i for i, diff in enumerate(results) if diff > 2 * math.sqrt(n))]
        print(f"RESULT: FALSIFIED counterexample=\"mean_diff > 2 * sqrt(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unmet_acceptance_criterion")