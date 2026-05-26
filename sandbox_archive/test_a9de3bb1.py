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
    
    def generate_clause_set(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def noncommutative_lp_norm(clauses, p):
        n = len(clauses[0])
        m = len(clauses)
        total = sum(abs(sum(clause))**p for clause in clauses)
        return (total / m)**(1/p)
    
    def dpll_disjointness(clauses):
        n = len(clauses[0])
        stack = [(0, [False] * n)]
        while stack:
            i, assignment = stack.pop()
            if i == n:
                if all(x != y for x, y in zip(assignment[:n//2], assignment[n//2:])):
                    return True
                continue
            for val in [True, False]:
                new_assignment = assignment[:]
                new_assignment[i] = val
                stack.append((i + 1, new_assignment))
        return False
    
    def communication_complexity(clauses):
        n = len(clauses[0])
        m = len(clauses)
        cc = 0
        for _ in range(10):  # Sample multiple times to get a good estimate
            assignment = [random.choice([True, False]) for _ in range(n)]
            if dpll_disjointness(clauses):
                cc += 1
        return cc / 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * 10)
        clauses = generate_clause_set(n, m)
        lp_norm = noncommutative_lp_norm(clauses, p=2)
        cc = communication_complexity(clauses)
        results.append((n, lp_norm, cc))
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_lp_norm = sum(result[1] for result in results) / len(results)
    mean_cc = sum(result[2] for result in results) / len(results)
    
    if mean_lp_norm**(1/2) <= mean_cc:
        return {
            "metric_name": "communication_complexity",
            "metric_value": mean_cc,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "communication_complexity",
            "metric_value": mean_cc,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Counterexample found: n={n_values[0]}, lp_norm={mean_lp_norm}, cc={mean_cc}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Counterexample found\" first_failing_seed={first_failing_seed}")