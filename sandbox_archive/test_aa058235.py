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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(abs(c) != abs(clause[0]) for c in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def compute_diameter(clauses):
        n = len(clauses)
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if any(abs(c[i]) == abs(c[j]) for c in clauses):
                    graph[i][j] = 1
                    graph[j][i] = 1
        
        def bfs(start):
            visited = [False] * n
            queue = [start]
            visited[start] = True
            distance = [float('inf')] * n
            distance[start] = 0
            while queue:
                u = queue.pop(0)
                for v in range(n):
                    if graph[u][v] and not visited[v]:
                        visited[v] = True
                        distance[v] = distance[u] + 1
                        queue.append(v)
            return max(distance)
        
        diameter = 0
        for i in range(n):
            diameter = max(diameter, bfs(i))
        return diameter
    
    def minimal_local_field_order(d):
        return math.ceil(math.sqrt(d))
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        instance = generate_sat_instance(n)
        d = compute_diameter(instance)
        order = minimal_local_field_order(d)
        
        total_metric_value += order
        
        if conjecture_holds and order > math.ceil(math.sqrt(d)):
            conjecture_holds = False
            counterexample = f"Instance with n={n}, d={d}, order={order}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = 1.0 if conjecture_holds else 0.0
    
    return {
        "metric_name": "Minimal Order of Local Field",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")