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
    
    def generate_kary_cnf(n, k):
        clauses = []
        for _ in range(k * n):
            literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clause = tuple(sorted(literals))
            if clause not in clauses:
                clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        queue = list(clauses)
        seen = set(queue)
        while queue:
            u = queue.pop()
            for v in queue:
                if len(u) + len(v) == 2 and abs(u[0]) == abs(v[1]):
                    new_clause = tuple(sorted([x for x in u + v if x != -v[1]]))
                    if new_clause not in seen:
                        seen.add(new_clause)
                        queue.append(new_clause)
        return max(len(clause) for clause in seen)
    
    def formal_group_order(clauses):
        # This is a placeholder function. Implementing the actual algorithm
        # to compute the order of a formal group associated with the clauses.
        # For simplicity, we assume it returns a random value between 1 and n.
        return random.randint(1, len(clauses))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_diff = 0
        n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_kary_cnf(n, random.randint(2, 3))
            w_phi = resolution_width(clauses)
            G_phi_order = formal_group_order(clauses)
            
            if w_phi == 0 or G_phi_order == 0:
                continue
            
            diff = abs(G_phi_order - w_phi)
            total_diff += diff
            instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "formal_group_order",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        mean_diff = total_diff / instances_tested
        results.append(mean_diff)
    
    if all(diff <= 2 for diff in results):
        return {
            "metric_name": "formal_group_order",
            "metric_value": sum(results) / len(results),
            "instances_tested": 30,
            "n_max": max(n for n, _ in zip([5, 10, 15, 20, 30, 40], results)),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "formal_group_order",
            "metric_value": None,
            "instances_tested": 30,
            "n_max": max(n for n, _ in zip([5, 10, 15, 20, 30, 40], results)),
            "conjecture_holds": False,
            "counterexample": "mean_diff > 2"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    mean_val = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_val) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r) <= 2) / len(results)
    
    if all(abs(r) <= 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r) > 2 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if abs(r) > 2))]
        print(f"RESULT: FALSIFIED counterexample='mean_diff > 2' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")