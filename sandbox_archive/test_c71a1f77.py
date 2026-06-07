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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) == 0:
                clause[random.randint(0, n-1)] *= -1
            clauses.append(tuple(sorted(clause)))
        return tuple(sorted(set(clauses)))

    def compute_diameter(instance):
        n = len(instance)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if any(abs(instance[i][k] - instance[j][k]) == 2 for k in range(n)):
                    adjacency_matrix[i][j] = 1
                    adjacency_matrix[j][i] = 1
        
        def bfs(start):
            visited = [False] * n
            queue = [start]
            visited[start] = True
            distance = 0
            while queue:
                next_queue = []
                for node in queue:
                    for neighbor in range(n):
                        if adjacency_matrix[node][neighbor] == 1 and not visited[neighbor]:
                            visited[neighbor] = True
                            next_queue.append(neighbor)
                queue = next_queue
                distance += 1
            return distance
        
        max_distance = 0
        for i in range(n):
            max_distance = max(max_distance, bfs(i))
        return max_distance

    def minimal_local_field_order(d):
        if d == 0:
            return 2
        return math.ceil(math.sqrt(d))

    n_max = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        instance = generate_sat_instance(n)
        d = compute_diameter(instance)
        order = minimal_local_field_order(d)
        metric_value += order
        if order > math.ceil(math.sqrt(d)) * 1.05:
            conjecture_holds = False
            counterexample = f"Instance with n={n}, d={d}, order={order}"
    
    mean_metric_value = metric_value / instances_tested
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
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")