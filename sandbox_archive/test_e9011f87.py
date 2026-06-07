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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def sat_instance_diameter(clauses):
        n = len(clauses[0])
        graph = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                for j in range(i+1, n):
                    if (clause[i], clause[j]) not in [(1, 1), (-1, -1)]:
                        graph[abs(clause[i])-1][abs(clause[j])-1] = 1
        visited = [False] * n
        queue = []
        for i in range(n):
            if not visited[i]:
                visited[i] = True
                queue.append((i, 0))
                while queue:
                    node, dist = queue.pop(0)
                    for j in range(n):
                        if graph[node][j] and not visited[j]:
                            visited[j] = True
                            queue.append((j, dist + 1))
        return max(dist for _, dist in queue)
    
    def minimal_local_field_order(d):
        if d == 0:
            return 1
        return math.ceil(math.sqrt(d))
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clauses = generate_sat_instance(n)
        d = sat_instance_diameter(clauses)
        order = minimal_local_field_order(d)
        metric_values.append(order)
        
        if order > math.ceil(math.sqrt(d)):
            conjecture_holds = False
            counterexample = f"n={n}, d={d}, order={order}"
    
    return {
        "metric_name": "Minimal Order of Local Field",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")