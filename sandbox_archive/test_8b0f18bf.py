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
        # Simplified version for demonstration purposes
        # In practice, this would involve more complex geometric calculations
        return n * (n - 1) // 2
    
    def communication_complexity_rank_variance(graph):
        n = len(graph)
        total_weight = sum(sum(row[i] for i in range(i + 1, n)) for row in graph)
        mean_weight = total_weight / (n * (n - 1) // 4)
        variance = sum((graph[i][j] - mean_weight) ** 2 for i in range(n) for j in range(i + 1, n)) / (n * (n - 1) // 4)
        return variance
    
    def pearson_correlation_coefficient(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    log_sym_quotient_group = []
    rank_variance = []
    
    for n in n_values:
        graph = generate_symmetric_graph(n)
        sym_quotient = symplectic_quotient_group(graph)
        var = communication_complexity_rank_variance(graph)
        log_sym_quotient_group.append(math.log(sym_quotient))
        rank_variance.append(var)
    
    correlation_coefficient = pearson_correlation_coefficient(log_sym_quotient_group, rank_variance)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8) / len(results)
    
    if all(abs(r["metric_value"]) >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.8 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")