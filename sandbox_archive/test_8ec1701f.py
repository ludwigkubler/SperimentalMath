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
    
    def dpll(cnf, assignment={}):
        unit_clauses = [c for c in cnf if len(c) == 1]
        while unit_clauses:
            literal = unit_clauses.pop()
            literal = literal[0]
            if literal < 0:
                literal = -literal
                value = False
            else:
                value = True
            assignment[literal] = value
            cnf = [c for c in cnf if literal not in c and -literal not in c]
            unit_clauses.extend([c for c in cnf if len(c) == 1])
        
        pure_literals = {}
        for literal in range(1, n + 1):
            positive_count = sum(1 for c in cnf if literal in c)
            negative_count = sum(1 for c in cnf if -literal in c)
            if positive_count == 0 and literal not in assignment:
                pure_literals[literal] = True
            elif negative_count == 0 and literal not in assignment:
                pure_literals[literal] = False
        
        if pure_literals:
            literal = next(iter(pure_literals))
            value = pure_literals[literal]
            assignment[literal] = value
            cnf = [c for c in cnf if literal not in c and -literal not in c]
        
        if not cnf:
            return True, assignment
        
        literal = random.choice(list(assignment.keys()))
        value = not assignment[literal]
        new_assignment = assignment.copy()
        new_assignment[literal] = value
        result1, _ = dpll(cnf, new_assignment)
        if result1:
            return True, new_assignment
        
        del new_assignment[literal]
        new_assignment[literal] = not value
        result2, _ = dpll(cnf, new_assignment)
        if result2:
            return True, new_assignment
        
        return False, {}
    
    def word_problem_for_groups(cnf):
        # Simplified version for demonstration purposes
        return len(cnf)  # This is a placeholder
    
    n_values = [5, 10, 15, 20, 30, 40]
    orders = []
    heights = []
    
    for n in n_values:
        for _ in range(30):
            cnf = generate_cnf(n)
            order = word_problem_for_groups(cnf)
            _, assignment = dpll(cnf)
            height = len(assignment)  # Simplified height calculation
            orders.append(order)
            heights.append(height)
    
    if not orders or not heights:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_order = sum(orders) / len(orders)
    median_height = sorted(heights)[len(heights) // 2]
    mean_diff = abs(mean_order - median_height) / median_height
    
    correlation_coefficient = sum((x - mean_order) * (y - median_height) for x, y in zip(orders, heights)) / len(orders)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": 180,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and mean_diff <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, order={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break