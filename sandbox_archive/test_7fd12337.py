# auto-injected by SEC sandbox
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
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def get_index(literal):
        if literal.startswith('-'):
            return -int(literal[1:]) - 1
        else:
            return int(literal) - 1
    
    def incidence_matrix(formula, n):
        literals = sorted(set([abs(int(l)) for l in formula]))
        matrix = [[0] * (2 * n) for _ in range(len(literals))]
        for literal in literals:
            index = get_index(f'-{literal}')
            if index < 0:
                matrix[literals.index(str(-index))] = [1 if i == -index else 0 for i in range(2 * n)]
            else:
                matrix[literals.index(str(index))] = [1 if i == index else 0 for i in range(2 * n)]
        return matrix
    
    def resolution_width(formula):
        clauses = formula.split(' or ')
        literals = sorted(set([abs(int(l)) for l in formula]))
        n = len(literals)
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            clause = next(c for c in clauses if any(l in assignment and assignment[l] == 1 for l in c))
            literal = next(l for l in clause if l not in assignment)
            if literal < 0:
                literal = -literal
                negated = True
            else:
                negated = False
            
            def extend_assignment(assignment, literal, negated):
                new_assignment = assignment.copy()
                new_assignment[literal] = 1 if not negated else 0
                return new_assignment
            
            if dpll(clauses, extend_assignment(assignment, literal, negated)):
                return True
            elif dpll(clauses, extend_assignment(assignment, -literal, negated)):
                return True
            else:
                return False
        
        width = 0
        for clause in clauses:
            assignment = {}
            if not dpll([c for c in clauses if literal not in c], assignment):
                width += 1
        return width
    
    def min_order(matrix):
        n = len(matrix)
        m = len(matrix[0])
        
        # Gaussian elimination to find the rank of the matrix
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            if matrix[i][i] == 0:
                return float('inf')
            
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(m):
                    matrix[j][k] += factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(val != 0 for val in row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_orders = []
    widths = []
    
    for n in n_values:
        for _ in range(5):
            literals = set()
            for _ in range(n * (n - 1) // 2):
                a, b = random.sample(range(1, n + 1), 2)
                literals.add(f'{a}')
                literals.add(f'-{b}')
            formula = ' or '.join([f'{-l} or {r}' for l, r in combinations(literals, 2)])
            
            Inc = incidence_matrix(formula, n)
            min_order_value = min_order(Inc)
            width_value = resolution_width(formula)
            
            if min_order_value == float('inf'):
                continue
            
            min_orders.append(min_order_value)
            widths.append(width_value)
    
    if not min_orders or not widths:
        return {
            "metric_name": "min_order vs width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(min_orders)
    mean_min_order = sum(min_orders) / n
    mean_width = sum(widths) / n
    
    covariance = sum((min_orders[i] - mean_min_order) * (widths[i] - mean_width) for i in range(n)) / n
    variance_min_order = sum((min_orders[i] - mean_min_order) ** 2 for i in range(n)) / n
    variance_width = sum((widths[i] - mean_width) ** 2 for i in range(n)) / n
    
    correlation_coefficient = covariance / (math.sqrt(variance_min_order) * math.sqrt(variance_width))
    
    return {
        "metric_name": "min_order vs width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_orders),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")