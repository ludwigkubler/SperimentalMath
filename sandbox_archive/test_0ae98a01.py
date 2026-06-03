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
    
    def is_planar(n, edges):
        if n < 3:
            return True
        max_edges = 3 * (n - 2)
        if len(edges) > max_edges:
            return False
        visited = [False] * n
        parent = [-1] * n
        
        def dfs(v, u):
            stack = [(v, u)]
            while stack:
                v, u = stack.pop()
                if visited[v]:
                    continue
                visited[v] = True
                for w in range(n):
                    if (w != v and w != u and (v, w) in edges or (w, v) in edges):
                        if parent[w] == -1:
                            parent[w] = v
                            stack.append((w, v))
                        elif parent[w] != u:
                            return False
            return True
        
        for i in range(n):
            if not visited[i]:
                if not dfs(i, -1):
                    return False
        return True
    
    def min_geometric_entropy(n, edges):
        if not is_planar(n, edges):
            return float('inf')
        
        # Encode positions of points in a unit square
        positions = [(random.random(), random.random()) for _ in range(n)]
        
        # Calculate the minimum number of bits required to encode these positions
        entropy = 0
        for pos in positions:
            x, y = pos
            entropy += math.ceil(math.log2(1 / (x * (1 - x) * y * (1 - y))))
        return entropy
    
    def communication_complexity_rank(n, edges):
        if not is_planar(n, edges):
            return float('inf')
        
        # Determine the smallest value of k such that any function f defined on G can be computed with communication complexity O(k)
        # This is a simplified version and may not accurately reflect actual communication complexity
        rank = 0
        for i in range(1, n + 1):
            if (i * (i - 1)) // 2 <= len(edges) < ((i + 1) * i) // 2:
                rank = i
                break
        return rank
    
    def correlation_coefficient(data1, data2):
        n = len(data1)
        mean1 = sum(data1) / n
        mean2 = sum(data2) / n
        cov = sum((data1[i] - mean1) * (data2[i] - mean2) for i in range(n)) / n
        var1 = sum((data1[i] - mean1) ** 2 for i in range(n)) / n
        var2 = sum((data2[i] - mean2) ** 2 for i in range(n)) / n
        return cov / (math.sqrt(var1) * math.sqrt(var2))
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    r_values = []
    
    for n in n_values:
        edges = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n * (n - 1) // 2)]
        if not is_planar(n, edges):
            continue
        
        h = min_geometric_entropy(n, edges)
        r = communication_complexity_rank(n, edges)
        
        if h == float('inf') or r == float('inf'):
            continue
        
        h_values.append(h)
        r_values.append(r)
    
    if not h_values or not r_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = correlation_coefficient(h_values, r_values)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 1 for i in range(5, 35)]
    
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")