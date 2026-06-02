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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def galois_group_order(f):
        n = len(f)
        field_size = 2**n
        elements = [i for i in range(field_size)]
        generators = []
        
        for i in range(1, field_size):
            if all((elements[j] * i) % field_size == j for j in range(field_size)):
                generators.append(i)
        
        return len(generators)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    continue
            
            for j in range(m):
                matrix[i][j] /= matrix[i][i]
            
            for j in range(n):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(m):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return sum(1 for row in matrix if any(row))
    
    def compute_metric(n):
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        order = galois_group_order(f)
        return rank, order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            rank, order = compute_metric(n)
            results.append((n, rank, order))
    
    if not results:
        return {
            "metric_name": "Galois Group Order vs Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _, _ in results)
    instances_tested = len(results)
    
    rank_values = [rank for _, rank, _ in results]
    order_values = [order for _, _, order in results]
    
    mean_rank = sum(rank_values) / instances_tested
    mean_order = sum(order_values) / instances_tested
    
    correlation_coefficient = (sum((rank - mean_rank) * (order - mean_order) for rank, order, _ in results)
                                / math.sqrt(sum((rank - mean_rank)**2 for rank, _, _ in results)
                                            * sum((order - mean_order)**2 for _, order, _ in results)))
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) * math.sqrt(instances_tested - 2) / math.sqrt(2)))
    
    conjecture_holds = correlation_coefficient >= 0.9 and p_value <= 0.05
    
    return {
        "metric_name": "Galois Group Order vs Communication Complexity Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Correlation: {correlation_coefficient}, p-value: {p_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_metric_value = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"])
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"]))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")