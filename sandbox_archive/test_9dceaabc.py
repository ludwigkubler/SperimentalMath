# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_symmetric_graph(n):
        # Generate a random symmetric graph with n vertices
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    adj_matrix[i][j] = adj_matrix[j][i] = random.randint(1, 10)
        return adj_matrix
    
    def is_symmetric(matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] != matrix[j][i]:
                    return False
        return True
    
    def symplectic_quotient_size(adj_matrix):
        # Simulate the computation of the symplectic quotient group size
        # This is a placeholder function and should be replaced with actual logic
        n = len(adj_matrix)
        return n * (n - 1) // 2
    
    def communication_complexity_rank_variance(adj_matrix):
        # Simulate the computation of the communication complexity rank variance
        # This is a placeholder function and should be replaced with actual logic
        n = len(adj_matrix)
        return sum(sum(row) for row in adj_matrix) / (n * n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    log_symplectic_quotient = []
    r_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        graph = generate_symmetric_graph(n)
        if not is_symmetric(graph):
            continue
        
        symplectic_group_size = symplectic_quotient_size(graph)
        r_value = communication_complexity_rank_variance(graph)
        
        log_symplectic_quotient.append(Fraction(symplectic_group_size).log2())
        r_values.append(r_value)
        instances_tested += 1
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "symplectic_quotient_log2",
            "metric_value": sum(log_symplectic_quotient) / len(log_symplectic_quotient),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    pearson_corr = 0
    for i in range(instances_tested):
        pearson_corr += (log_symplectic_quotient[i] - sum(log_symplectic_quotient) / instances_tested) * \
                         (r_values[i] - sum(r_values) / instances_tested)
    
    pearson_corr /= instances_tested * (sum(x**2 for x in log_symplectic_quotient) / instances_tested - sum(log_symplectic_quotient)**2 / instances_tested) ** 0.5 * \
                    (sum(x**2 for x in r_values) / instances_tested - sum(r_values)**2 / instances_tested) ** 0.5
    
    return {
        "metric_name": "symplectic_quotient_log2",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(pearson_corr) >= 0.8,
        "counterexample": "" if abs(pearson_corr) >= 0.8 else f"low_correlation:{pearson_corr}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=NA support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.8 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.8)
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")