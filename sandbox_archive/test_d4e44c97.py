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
    
    def generate_communication_instance(rank):
        # Generate a simple communication complexity instance with given rank
        n = 2 * rank + 1
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if (i + j) % 2 == 0:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def compute_minimal_order(graph):
        # Compute the minimal order of an affine divisor for a given graph
        n = len(graph)
        if n <= 1:
            return 0
        
        # Gaussian elimination to find rank
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(i, n):
                if graph[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            
            # Swap rows to put the pivot at the top
            graph[i], graph[pivot_row] = graph[pivot_row], graph[i]
            
            # Eliminate other rows
            for j in range(n):
                if i != j and graph[j][i] != 0:
                    factor = Fraction(graph[j][i], graph[i][i])
                    for k in range(i, n):
                        graph[j][k] -= factor * graph[i][k]
            
            rank += 1
        
        return rank
    
    def pearson_correlation(x, y):
        # Compute Pearson correlation coefficient
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        var_x = sum((x[i] - mean_x)**2 for i in range(n))
        var_y = sum((y[i] - mean_y)**2 for i in range(n))
        
        if var_x == 0 or var_y == 0:
            return 0
        
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    ranks = [5, 10, 15, 20, 30, 40]
    orders = []
    
    for rank in ranks:
        graph = generate_communication_instance(rank)
        order = compute_minimal_order(graph)
        orders.append(order)
    
    correlation = pearson_correlation(ranks, orders)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(ranks),
        "conjecture_holds": abs(correlation) >= 0.95,
        "counterexample": "" if abs(correlation) >= 0.95 else f"Correlation {correlation} is too low"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")