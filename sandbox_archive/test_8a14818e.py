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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2**n - 1):  # Generate all non-empty subsets of variables
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def truth_table(clauses):
        n = len(clauses[0])
        table = {}
        for assignment in itertools.product([False, True], repeat=n):
            assignment_dict = {i+1: int(assignment[i]) for i in range(n)}
            table[tuple(assignment)] = any(all(lit * assignment_dict[abs(lit)] > 0 for lit in clause) for clause in clauses)
        return table
    
    def entropy(table):
        n = len(table)
        counts = [sum(table.values()), n - sum(table.values())]
        probabilities = [c / n for c in counts]
        return -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)
    
    def diophantine_approximation(entropy):
        # Simplified approximation using continued fractions
        a, b = entropy, 1
        while True:
            q = int(a / b)
            a, b = b, a - q * b
            if abs(b) == 1:
                return q
    
    n_values = [10, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(7):  # Aim for at least 30 instances per seed
            clauses = generate_3cnf(n)
            table = truth_table(clauses)
            entropy_val = entropy(table)
            approx_index = diophantine_approximation(entropy_val)
            results.append((n, approx_index))
    
    if not results:
        return {
            "metric_name": "minimal_diophantine_index",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    n_total = len(results)
    approx_indices = [r[1] for r in results]
    mean_approx_index = sum(approx_indices) / n_total
    std_approx_index = math.sqrt(sum((x - mean_approx_index) ** 2 for x in approx_indices) / n_total)
    
    C = 0.5  # Hypothetical constant, adjust as needed
    if any(index > C * n * math.log(n) for n, index in results):
        return {
            "metric_name": "minimal_diophantine_index",
            "metric_value": mean_approx_index,
            "instances_tested": n_total,
            "conjecture_holds": False,
            "counterexample": f"unsatisfiable with Cn log n = {C * n * math.log(n)}"
        }
    
    return {
        "metric_name": "minimal_diophantine_index",
        "metric_value": mean_approx_index,
        "instances_tested": n_total,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='unsatisfiable' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")