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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = clause[1], clause[0]
        cnf.append(clause)
    return cnf

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        pivot_row = i
        for r in range(i + 1, rows):
            if abs(matrix[r][i]) > abs(matrix[pivot_row][i]):
                pivot_row = r
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Eliminate below the pivot
        for r in range(i + 1, rows):
            factor = -matrix[r][i] / matrix[i][i]
            if factor == 0:
                continue
            for c in range(cols):
                matrix[r][c] += factor * matrix[i][c]
    
    # Back-substitute to find the solution
    solution = [0] * cols
    for i in range(rows - 1, -1, -1):
        if matrix[i][i] == 0:
            return None  # Singular matrix
        solution[i] = matrix[i][-1] / matrix[i][i]
        for r in range(i - 1, -1, -1):
            matrix[r][-1] -= matrix[r][i] * solution[i]
    return solution

def monodromy_group_order(cnf):
    n = len(cnf)
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
        if clause[0] > 0 and clause[1] > 0:
            matrix[i][j] += 1
        elif clause[0] < 0 and clause[1] < 0:
            matrix[i][j] -= 1
        elif clause[0] > 0 and clause[1] < 0:
            matrix[i][j + n] += 1
        else:
            matrix[i + n][j] += 1
    
    rank = 0
    for i in range(n):
        if gaussian_elimination(matrix[:i+1]) is not None:
            rank += 1
    return rank

def resolution_width(cnf):
    stack = []
    while cnf:
        clause = cnf.pop()
        if len(clause) == 1:
            return -1
        unit_clause = next((c for c in clause if abs(c) not in [abs(lit) for lit in stack]), None)
        if unit_clause is None:
            return -1
        polarity = unit_clause > 0
        literal = abs(unit_clause)
        cnf = [c for c in cnf if literal not in c]
        for i, other_clause in enumerate(cnf):
            if literal in other_clause:
                cnf[i] = [l for l in other_clause if l != -literal]
            elif -literal in other_clause:
                cnf[i].append(-polarity * literal)
        stack.append(unit_clause)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        m = random.randint(n * 2, n * 10)
        cnf = generate_cnf(n, m)
        
        try:
            monodromy_order = monodromy_group_order(cnf)
            width = resolution_width(cnf)
            if monodromy_order is not None and width != -1:
                metric_values.append((monodromy_order, width))
        except Exception as e:
            return {
                "metric_name": "Monodromy Group Order vs Resolution Width",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    
    if not metric_values:
        return {
            "metric_name": "Monodromy Group Order vs Resolution Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    monodromy_orders, widths = zip(*metric_values)
    mean_order = sum(monodromy_orders) / len(monodromy_orders)
    mean_width = sum(widths) / len(widths)
    
    return {
        "metric_name": "Monodromy Group Order vs Resolution Width",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,  # This will be checked in the main block
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 17 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE no_valid_instances")
    else:
        mean_value = sum(r["metric_value"] for r in results if "metric_value" in r and r["metric_value"] is not None) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample='not_enough_support' first_failing_seed={first_failing_seed}")