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
    
    def generate_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['&', '|'])
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f"({left} {op} {right})"
    
    def resolution_width(formula, variables):
        if formula in ['True', 'False']:
            return 1
        elif formula[0] == '(' and formula[-1] == ')':
            op = formula[3]
            left = resolution_width(formula[1:formula.index(')')], variables)
            right = resolution_width(formula[formula.index(')')+2:], variables)
            return max(left, right) + 1
        else:
            var = formula.strip()
            if var in variables:
                return 1
            else:
                return 0
    
    def matrix_algebra(formula):
        n = len(set(formula.split()))
        A = [[0] * n for _ in range(n)]
        for i, char in enumerate(formula):
            if char.isalpha():
                A[i][i] = 1
        return A
    
    def aut_order(matrix):
        n = len(matrix)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        count = 0
        
        def matrix_multiplication(A, B):
            result = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        result[i][j] += A[i][k] * B[k][j]
            return result
        
        def is_equal(A, B):
            for i in range(n):
                for j in range(n):
                    if A[i][j] != B[i][j]:
                        return False
            return True
        
        for perm in itertools.permutations(range(n)):
            permuted_matrix = [[matrix[perm[i]][perm[j]] for j in range(n)] for i in range(n)]
            if is_equal(permuted_matrix, identity):
                count += 1
        
        return count
    
    def log_aut_order(matrix):
        order = aut_order(matrix)
        if order == 0:
            return float('-inf')
        return math.log(order)
    
    n_values = [5, 10, 15, 20, 30, 40]
    widths = []
    log_orders = []
    
    for n in n_values:
        formula = generate_formula(n)
        variables = set(formula.split())
        width = resolution_width(formula, list(variables))
        matrix = matrix_algebra(formula)
        log_order = log_aut_order(matrix)
        
        widths.append(width)
        log_orders.append(log_order)
    
    correlation_coefficient = 0
    for i in range(len(n_values)):
        for j in range(i + 1, len(n_values)):
            correlation_coefficient += (widths[i] - widths[j]) * (log_orders[i] - log_orders[j])
    correlation_coefficient /= (len(n_values) * (len(n_values) - 1))
    
    mean_width = sum(widths) / len(widths)
    mean_log_order = sum(log_orders) / len(log_orders)
    
    if abs(correlation_coefficient) >= 0.8 and max(abs(mean_log_order - log_aut_order(matrix_algebra(generate_formula(n)))) for n in n_values) <= 3:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "correlation_coefficient < 0.8 or mean absolute difference > 3"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['n_max'] >= 16 for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
            print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=n_max < 16")