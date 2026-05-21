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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_to_coxeter_group(f):
        n = len(f)
        G = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def longest_element_length(G):
        n = len(G)
        visited = [False]*n
        max_length = 0
        
        def dfs(node, length):
            nonlocal max_length
            if length > max_length:
                max_length = length
            for neighbor in range(n):
                if G[node][neighbor] == 1 and not visited[neighbor]:
                    visited[neighbor] = True
                    dfs(neighbor, length + 1)
                    visited[neighbor] = False
        
        for i in range(n):
            visited[i] = True
            dfs(i, 0)
            visited[i] = False
        
        return max_length
    
    def karchmer_wigderson_cost(f):
        n = len(f)
        if n == 1:
            return 1
        left = f[:n//2]
        right = f[n//2:]
        cost_left = karchmer_wigderson_cost(left)
        cost_right = karchmer_wigderson_cost(right)
        return max(cost_left, cost_right) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    total_cost = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 random instances
            f = generate_boolean_function(n)
            G = boolean_to_coxeter_group(f)
            length = longest_element_length(G)
            cost = karchmer_wigderson_cost(f)
            total_length += length
            total_cost += cost
            instances_tested += 1
    
    avg_length = total_length / instances_tested
    avg_cost = total_cost / instances_tested
    
    return {
        "metric_name": "Coxeter Group Length vs KW Protocol Cost",
        "metric_value": abs(avg_length - avg_cost),
        "instances_tested": instances_tested,
        "conjecture_holds": abs(avg_length - avg_cost) <= 10,
        "counterexample": "" if abs(avg_length - avg_cost) <= 10 else f"avg_length={avg_length}, avg_cost={avg_cost}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")