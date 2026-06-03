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
    
    def min_simple_connected_components(f):
        n = len(f)
        visited = [False] * (2**n)
        components = 0
        
        def dfs(v):
            stack = [v]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    for i in range(n):
                        if f[v ^ (1 << i)] != f[u ^ (1 << i)] and not visited[u ^ (1 << i)]:
                            stack.append(u ^ (1 << i))
        
        for v in range(2**n):
            if not visited[v]:
                dfs(v)
                components += 1
        return components
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        
        def binary_search(left, right):
            while left < right:
                mid = (left + right) // 2
                if any(f[i] != f[j] for i in range(2**n) for j in range(i+1, 2**n) if (i ^ j) & ((1 << mid) - 1) == 0):
                    left = mid + 1
                else:
                    right = mid
            return left
        
        rank = binary_search(0, n)
        return rank
    
    def pearson_correlation_coefficient(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_order_values = []
    communication_complexity_rank_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        min_order = min_simple_connected_components(f)
        rank = communication_complexity_rank(f)
        
        min_order_values.append(min_order)
        communication_complexity_rank_values.append(rank)
    
    correlation_coefficient = pearson_correlation_coefficient(min_order_values, communication_complexity_rank_values)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": "" if abs(correlation_coefficient) >= 0.5 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient too low\" first_failing_seed={first_failing_seed}")