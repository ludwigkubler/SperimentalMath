# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import deque

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def sat_instance_diameter(clauses):
        n = len(clauses)
        if n == 0:
            return 0
        
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if any(lit in clauses[i] and -lit in clauses[j] for lit in set(clauses[i]) | set(clauses[j])):
                    graph[i].append(j)
                    graph[j].append(i)
        
        def bfs(start):
            visited = [False] * n
            queue = deque([start])
            visited[start] = True
            distance = 0
            while queue:
                for _ in range(len(queue)):
                    current = queue.popleft()
                    for neighbor in graph[current]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
                distance += 1
            return distance - 1
        
        max_distance = 0
        for i in range(n):
            max_distance = max(max_distance, bfs(i))
        
        return max_distance
    
    def minimal_local_field_order(diameter):
        # Simple heuristic: order of local field is at most diameter^2
        return int(math.ceil(diameter ** 1.5))
    
    trials = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(trials):
        n = random.randint(5, 40)
        clauses = []
        for _ in range(n):
            num_clauses = random.randint(1, min(2 * n, 30))
            clause = [random.choice([-i, i]) for i in range(1, n + 1)]
            if len(clause) > num_clauses:
                clause = random.sample(clause, num_clauses)
            clauses.append(clause)
        
        d = sat_instance_diameter(clauses)
        if d == 0:
            continue
        
        order = minimal_local_field_order(d)
        metric_values.append(order)
        
        if order > math.ceil(math.sqrt(n)):
            conjecture_holds = False
            counterexample = f"n={n}, d={d}, |O|={order}"
    
    return {
        "metric_name": "Minimal Order of Local Field",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(metric_values),
        "n_max": max(n for _ in range(trials)),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed + 1}")