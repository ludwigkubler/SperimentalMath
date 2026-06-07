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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            op = random.choice(['&', '|'])
            return f'({subformulas[0]} {op} {subformulas[1]})'
    
    def evaluate_formula(formula):
        if formula == '0':
            return 0
        elif formula == '1':
            return 1
        else:
            left, op, right = formula.split()
            left_val = evaluate_formula(left)
            right_val = evaluate_formula(right)
            if op == '&':
                return left_val & right_val
            elif op == '|':
                return left_val | right_val
    
    def generate_matroid(formula):
        n = formula.count('(') + 1
        matroid = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if evaluate_formula(f'({formula[:i]} {chr(97+i)} {formula[i+1:j]} {chr(97+j)})') != evaluate_formula(f'({formula[:i]} {chr(97+i)} {formula[i+1:j]} {chr(97+j-1)})'):
                    matroid[i][j] = 1
        return matroid
    
    def calculate_hodge_index(matroid):
        n = len(matroid)
        rank = sum(max(sum(row[:i]) for row in matroid) for i in range(n))
        hodge_index = (rank * (n - rank)) / (n * (n - 1))
        return hodge_index
    
    def calculate_rank_variance(matroid):
        n = len(matroid)
        ranks = [sum(row[:i]) for row in matroid]
        mean_rank = sum(ranks) / n
        variance = sum((rank - mean_rank) ** 2 for rank in ranks) / (n - 1)
        return variance
    
    def generate_communication_matrix(formula):
        n = formula.count('(') + 1
        communication_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if evaluate_formula(f'({formula[:i]} {chr(97+i)} {formula[i+1:j]} {chr(97+j)})') != evaluate_formula(f'({formula[:i]} {chr(97+i)} {formula[i+1:j]} {chr(97+j-1)})'):
                    communication_matrix[i][j] = 1
        return communication_matrix
    
    def calculate_rank_variances(communication_matrix):
        n = len(communication_matrix)
        ranks = [sum(row[:i]) for row in communication_matrix]
        rank_variances = []
        for i in range(n):
            submatrix = [row[:i] for row in communication_matrix]
            submatrix_rank = sum(max(sum(subrow[:j]) for subrow in submatrix) for j in range(i+1))
            rank_variances.append((submatrix_rank * (i - submatrix_rank)) / (i * (i - 1)))
        return rank_variances
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / (n - 1))
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / (n - 1))
        return covariance / (std_dev_x * std_dev_y)
    
    def linear_regression(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        slope = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / sum((x[i] - mean_x) ** 2 for i in range(n))
        intercept = mean_y - slope * mean_x
        return slope, intercept
    
    n_max = 40
    instances_tested = 30
    hodge_indices = []
    rank_variances = []
    
    for _ in range(instances_tested):
        formula = generate_boolean_formula(random.randint(5, n_max))
        matroid = generate_matroid(formula)
        hodge_index = calculate_hodge_index(matroid)
        communication_matrix = generate_communication_matrix(formula)
        rank_variance = calculate_rank_variances(communication_matrix)
        hodge_indices.append(hodge_index)
        rank_variances.append(rank_variance)
    
    correlation_coefficient, _ = linear_regression(hodge_indices, rank_variances)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.7 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) > 0.7 and p_value < 0.05) / len(results)
    
    if all(abs(r["metric_value"]) > 0.7 and p_value < 0.05 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not (abs(r["metric_value"]) > 0.7 and p_value < 0.05) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (abs(result["metric_value"]) > 0.7 and p_value < 0.05))
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")