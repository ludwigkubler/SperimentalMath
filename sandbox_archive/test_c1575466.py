# auto-injected by SEC sandbox
import math
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
from fractions import Fraction
from itertools import combinations, permutations

def generate_cnf(n, m):
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def min_order(cnf):
    variables = set()
    for clause in cnf:
        variables.update(clause)
    n = len(variables)
    partitions = []
    
    def is_valid_partition(partition):
        for subset in partition:
            if not any(x in subset for x in variables):
                return False
        return True
    
    def generate_partitions(current_partition, remaining_variables):
        if not remaining_variables:
            if is_valid_partition(current_partition):
                partitions.append(current_partition)
            return
        new_subset = set()
        for var in remaining_variables:
            new_subset.add(var)
            generate_partitions(current_partition + [new_subset], remaining_variables - {var})
    
    generate_partitions([], variables)
    min_order_value = float('inf')
    for partition in partitions:
        if len(partition) < min_order_value:
            min_order_value = len(partition)
    return min_order_value

def resolution_width(cnf):
    clauses = cnf[:]
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if len(set(clauses[i]) & set(clauses[j])) == 1:
                    new_clause = [x for x in clauses[i] if x not in clauses[j]] + \
                                  [x for x in clauses[j] if x not in clauses[i]]
                    if -new_clause[0] in new_clause:
                        return len(new_clauses) + 1
                    new_clauses.append(new_clause)
        if new_clauses == clauses:
            break
        clauses = new_clauses
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    min_order_values = []
    widths = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(n, 2 * n))
            min_order_value = min_order(cnf)
            width = resolution_width(cnf)
            if min_order_value is not None and width is not None:
                min_order_values.append(min_order_value)
                widths.append(width)
                instances_tested += 1
    
    correlation_coefficient = sum((x - sum(min_order_values) / len(min_order_values)) * 
                                   (y - sum(widths) / len(widths)) for x, y in zip(min_order_values, widths)) / \
                              (len(min_order_values) * sum((x - sum(min_order_values) / len(min_order_values)) ** 2 for x in min_order_values) *
                               sum((y - sum(widths) / len(widths)) ** 2 for y in widths)) ** 0.5
    
    conjecture_holds = abs(correlation_coefficient) >= 0.7 and max(min_order_values) / max(widths) <= 1.5
    counterexample = "" if conjecture_holds else "correlation_threshold_not_met"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")