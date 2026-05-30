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
    n = 30
    instances_tested = 0
    total_distance = 0.0
    max_n = 0
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment={}):
        unassigned_vars = [var for var in range(1, n + 1) if var not in assignment and -var not in assignment]
        if not unassigned_vars:
            return all(clause_evaluated(clause, assignment) for clause in clauses)
        var = random.choice(unassigned_vars)
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if dpll(clauses, new_assignment):
                return True
        return False
    
    def clause_evaluated(clause, assignment):
        return any(assignment.get(abs(lit), False) == (lit > 0) for lit in clause)
    
    def kendall_tau_distance(freqs):
        n = len(freqs)
        tau_numerator = sum((freqs[i] - freqs[j]) * (i - j) for i in range(n) for j in range(i + 1, n))
        tau_denominator = (n * (n - 1)) / 2
        return abs(tau_numerator) / tau_denominator
    
    for _ in range(30):
        clauses = generate_3cnf(n)
        if not dpll(clauses):
            continue
        instances_tested += 1
        literal_freqs = [0] * (2 * n + 1)
        for clause in clauses:
            for lit in clause:
                literal_freqs[abs(lit)] += 1
        total_distance += kendall_tau_distance(literal_freqs)
        max_n = max(max_n, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "Kendall tau distance",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_distance = total_distance / instances_tested
    expected_distance = n ** 0.5
    return {
        "metric_name": "Kendall tau distance",
        "metric_value": mean_distance,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": abs(mean_distance - expected_distance) <= 0.5 and all(d <= n ** 0.5 + 1 for d in [kendall_tau_distance(literal_freqs) for _ in range(30)]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_distance = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_distance} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")