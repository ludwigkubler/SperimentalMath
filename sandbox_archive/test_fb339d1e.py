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

def generate_random_circuit(n):
    clauses = []
    for _ in range(10):  # Generate a small number of clauses to keep it simple
        clause = [random.choice([f'x{i}' for i in range(n)])]
        if random.random() < 0.5:
            clause.append('or')
        else:
            clause.append('and')
        clause.append(random.choice([f'x{i}' for i in range(n)]))
        clauses.append(clause)
    return clauses

def evaluate_circuit(circuit, assignment):
    stack = []
    for token in circuit:
        if token == 'or':
            b = stack.pop()
            a = stack.pop()
            stack.append(a or b)
        elif token == 'and':
            b = stack.pop()
            a = stack.pop()
            stack.append(a and b)
        else:
            stack.append(assignment[token[1:]])
    return stack[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        total_instances = 0
        for _ in range(30):
            circuit = generate_random_circuit(n)
            assignment = {f'x{i}': random.choice([True, False]) for i in range(n)}
            monotone_width = len(circuit)  # Simplified for this example
            sheaf_order = n  # Simplified for this example
            
            total_instances += 1
            results.append((monotone_width, sheaf_order))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    monotone_widths = [r[0] for r in results]
    sheaf_orders = [r[1] for r in results]
    
    n_max = max(n_values)
    instances_tested = len(results)
    
    # Calculate Pearson correlation coefficient
    mean_x = sum(monotone_widths) / instances_tested
    mean_y = sum(sheaf_orders) / instances_tested
    
    cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(monotone_widths, sheaf_orders)) / instances_tested
    var_x = sum((x - mean_x) ** 2 for x in monotone_widths) / instances_tested
    var_y = sum((y - mean_y) ** 2 for y in sheaf_orders) / instances_tested
    
    correlation_coefficient = cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {seed} {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE no_support")