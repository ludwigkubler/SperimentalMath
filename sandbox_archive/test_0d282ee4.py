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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_clause_satisfied(clause, assignment):
        return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)
    
    def evaluate_cnf(cnf, assignment):
        return all(is_clause_satisfied(clause, assignment) for clause in cnf)
    
    def generate_assignment(n):
        return [random.choice([True, False]) for _ in range(n)]
    
    def count_distinct_representations(cnf):
        n = len(cnf)
        assignments = set()
        for _ in range(2 ** n):
            assignment = generate_assignment(n)
            if evaluate_cnf(cnf, assignment):
                assignments.add(tuple(assignment))
        return len(assignments)
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            count = count_distinct_representations(cnf)
            metric_values.append(count)
            instances_tested += 1
    
    mean_value = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    upper_bound = 2 ** n_max / (n_max * math.log(n_max, 2) * math.log(math.log(n_max, 2), 2))
    
    conjecture_holds = all(count <= upper_bound + 3 * std_dev for count in metric_values)
    counterexample = "" if conjecture_holds else "upper_bound_violation"
    
    return {
        "metric_name": "distinct_representations",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "upper_bound_violation" for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"] == "upper_bound_violation")
        print(f"RESULT: FALSIFIED counterexample=\"upper bound violation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_or_budget_exceeded")