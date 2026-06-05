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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_group(n):
        while True:
            group = set()
            for _ in range(n):
                element = tuple(random.randint(0, 1) for _ in range(n))
                if element not in group and len(group) < n:
                    group.add(element)
            if len(group) == n:
                return group
    
    def generate_representation(group):
        n = len(group)
        representation = {}
        for g in group:
            matrix = [[0] * n for _ in range(n)]
            for i, j in enumerate(g):
                matrix[i][j] = 1
            representation[g] = matrix
        return representation
    
    def calculate_min_representation_order(representation):
        min_order = float('inf')
        for g in representation:
            order = sum(sum(row) for row in representation[g])
            if order < min_order:
                min_order = order
        return min_order
    
    def generate_matrix_product_problem(group, representation):
        n = len(group)
        matrix_product = [[0] * n for _ in range(n)]
        for g1 in group:
            for g2 in group:
                product = [sum(representation[g1][i][j] * representation[g2][j][k] for j in range(n)) % 2 for k in range(n)]
                matrix_product[group.index(g1)][group.index(g2)] = tuple(product)
        return matrix_product
    
    def calculate_communication_complexity_rank(matrix_product):
        n = len(matrix_product)
        rank = 0
        for i in range(n):
            if any(matrix_product[i][j] != 0 for j in range(i, n)):
                rank += 1
        return rank
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_representation_orders = []
    comm_rank_values = []
    
    for n in n_values:
        group = generate_group(n)
        representation = generate_representation(group)
        min_order = calculate_min_representation_order(representation)
        matrix_product = generate_matrix_product_problem(group, representation)
        comm_rank = calculate_communication_complexity_rank(matrix_product)
        
        min_representation_orders.append(min_order)
        comm_rank_values.append(comm_rank)
    
    correlation_coefficient = correlation(min_representation_orders, comm_rank_values)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.95,
        "counterexample": "" if correlation_coefficient > 0.95 else "Correlation coefficient is less than 0.95"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient is less than 0.95\" first_failing_seed={first_failing_seed}")