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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monomial_ideal_order(instance):
        n = len(instance)
        # Simplified version of Gröbner basis calculation
        ideal = set()
        for i in range(2**n):
            if instance[i] == 1:
                factors = []
                for j in range(n):
                    if (i >> j) & 1:
                        factors.append(j + 1)
                ideal.add(tuple(sorted(factors)))
        return len(ideal)
    
    def resolution_proof_width(instance):
        n = len(instance)
        # Simplified version of DPLL-based resolution solver
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
        stack = [clauses]
        while stack:
            clause = stack.pop()
            if not clause:
                return float('inf')
            literal = min(clause, key=lambda x: abs(x))
            new_clauses = []
            for c in stack:
                if literal in c:
                    continue
                if -literal in c:
                    stack.remove(c)
                else:
                    new_clause = [l for l in c if l != -literal]
                    new_clauses.append(new_clause)
            stack.extend(new_clauses)
        return len(stack)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_order = 0
        total_width = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_sat_instance(n)
            order = monomial_ideal_order(instance)
            width = resolution_proof_width(instance)
            if order == 0 or width == float('inf'):
                continue
            total_order += order
            total_width += width
            instances_tested += 1
        if instances_tested < 5:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
        avg_order = total_order / instances_tested
        avg_width = total_width / instances_tested
        results.append((avg_order, avg_width))
    
    if len(results) < 6:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": sum(r[1] for r in results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    # Calculate Pearson's correlation coefficient
    n = len(results)
    x_mean = sum(order for order, _ in results) / n
    y_mean = sum(width for _, width in results) / n
    numerator = sum((order - x_mean) * (width - y_mean) for order, width in results)
    denominator = math.sqrt(sum((order - x_mean)**2 for order, _ in results)) * math.sqrt(sum((width - y_mean)**2 for _, width in results))
    if denominator == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": n * 5,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    correlation = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": n * 5,
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_data\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")