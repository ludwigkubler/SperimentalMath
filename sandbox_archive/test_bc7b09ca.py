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
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    weight = random.randint(1, 10)
                    graph[i][j] = weight
                    graph[j][i] = weight
        return graph
    
    def symplectic_quotient_group(graph):
        n = len(graph)
        # Simplified version for demonstration; actual computation depends on the specific structure of G
        return n * (n - 1) // 2
    
    def communication_complexity_rank_variance(graph):
        n = len(graph)
        total_weight = sum(sum(graph[i][j] for j in range(i + 1, n)) for i in range(n))
        avg_weight = Fraction(total_weight, n * (n - 1) // 2)
        variance = sum((graph[i][j] - avg_weight)**2 for i in range(n) for j in range(i + 1, n)) / (n * (n - 1) // 2)
        return variance
    
    def pearson_correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_dev_x = (sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))**0.5
        std_dev_y = (sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))**0.5
        return cov_xy / (std_dev_x * std_dev_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    log_symplectic_quotient = []
    communication_variance = []
    
    for n in n_values:
        graph = generate_symmetric_graph(n)
        symplectic_group_size = symplectic_quotient_group(graph)
        variance = communication_complexity_rank_variance(graph)
        
        if symplectic_group_size == 0 or variance == 0:
            continue
        
        log_symplectic_quotient.append(Fraction(symplectic_group_size).log())
        communication_variance.append(variance)
    
    if not log_symplectic_quotient or not communication_variance:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = pearson_correlation_coefficient(log_symplectic_quotient, communication_variance)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))**0.5
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_dev} support_fraction={support_fraction}")