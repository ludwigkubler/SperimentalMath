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
    
    def generate_communication_problem(n):
        # Generate a random n-bit communication problem
        return [random.randint(0, 1) for _ in range(n)]
    
    def construct_groupoid(problem):
        # Construct a simple groupoid based on the communication problem
        groupoid = {}
        for i in range(len(problem)):
            for j in range(i + 1, len(problem)):
                if problem[i] != problem[j]:
                    key = (i, j)
                    if key not in groupoid:
                        groupoid[key] = set()
                    groupoid[key].add((problem[i], problem[j]))
        return groupoid
    
    def min_order(groupoid):
        # Compute the minimal order of elements in the groupoid
        orders = [len(values) for values in groupoid.values()]
        if not orders:
            return 0
        return min(orders)
    
    def communication_complexity(problem):
        # Compute the rank of the communication complexity
        n = len(problem)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if problem[i] != problem[j]:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(i + 1, n):
                            if matrix[j][i]:
                                matrix[j][i] -= row[i]
        return rank
    
    def pearson_correlation(x, y):
        # Compute the Pearson correlation coefficient
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        if std_x == 0 or std_y == 0:
            return 0
        return cov_xy / (std_x * std_y)
    
    correlation_coefficient = None
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            problem = generate_communication_problem(n)
            groupoid = construct_groupoid(problem)
            min_order_val = min_order(groupoid)
            comm_complexity_rank = communication_complexity(problem)
            
            if correlation_coefficient is None:
                correlation_coefficient = pearson_correlation([min_order_val], [comm_complexity_rank])
            else:
                correlation_coefficient += pearson_correlation([min_order_val], [comm_complexity_rank])
            
            instances_tested += 1
    
    if correlation_coefficient is not None:
        correlation_coefficient /= instances_tested
        conjecture_holds = 0.8 <= correlation_coefficient < 1.0
        counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")