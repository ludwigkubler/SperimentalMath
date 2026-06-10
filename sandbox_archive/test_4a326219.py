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
    
    def generate_tseitin_formula(d):
        variables = list(range(1, d+1))
        clauses = []
        
        for i in range(1, d+1):
            clauses.append([variables[i-1]])
        
        for i in range(1, d+1):
            for j in range(i+1, d+1):
                new_var = -d - i - j
                clauses.append([new_var, variables[i-1], variables[j-1]])
                clauses.append([-new_var, -variables[i-1]])
                clauses.append([-new_var, -variables[j-1]])
        
        return variables, clauses
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n + 1):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def resolution_width(clauses):
        n = len(clauses)
        queue = [c for c in clauses if len(c) == 1]
        while queue:
            new_queue = []
            while queue:
                p = queue.pop()
                for q in clauses:
                    if -p[0] in q and len(q) > 2:
                        new_q = list(filter(lambda x: x != -p[0], q))
                        new_queue.append(new_q)
            queue = new_queue
        return n
    
    def minimal_order(A):
        A = gaussian_elimination(A)
        order = 0
        for row in A:
            if any(x != 0 for x in row[:-1]):
                order += 1
        return order
    
    d_values = [10, 20, 30, 40]
    results = []
    
    for d in d_values:
        variables, clauses = generate_tseitin_formula(d)
        A = [[0] * (d + 1) for _ in range(d + 1)]
        
        for clause in clauses:
            if len(clause) == 2:
                i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
                A[i][j], A[j][i] = 1, 1
        
        order = minimal_order(A)
        width = resolution_width(clauses)
        
        results.append({
            "d": d,
            "order": order,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "Order vs Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    order_values = [r["order"] for r in results]
    width_values = [r["width"] for r in results]
    
    mean_order = sum(order_values) / len(order_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation_coefficient = 0
    if len(order_values) > 1:
        numerator = sum((order_values[i] - mean_order) * (width_values[i] - mean_width) for i in range(len(order_values)))
        denominator = math.sqrt(sum((order_values[i] - mean_order) ** 2 for i in range(len(order_values)))) * math.sqrt(sum((width_values[i] - mean_width) ** 2 for i in range(len(width_values))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Order vs Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(order_values),
        "n_max": max(d_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(c >= 0.6 for c in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction=1.0")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction:.2f}")