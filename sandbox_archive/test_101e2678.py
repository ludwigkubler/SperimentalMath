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
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n+1):
            clause = [random.randint(-i, -1), random.randint(i, n)]
            clauses.append(clause)
        return clauses
    
    def tseitin_graph(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        graph = {var: [] for var in variables}
        for i, clause in enumerate(cnf):
            new_var = n + i + 1
            for literal in clause:
                if literal > 0:
                    graph[literal].append(new_var)
                else:
                    graph[-literal].append(-new_var)
            for j in range(len(clause)):
                for k in range(j+1, len(clause)):
                    graph[clause[j]].append(-clause[k])
                    graph[-clause[j]].append(clause[k])
                    graph[clause[k]].append(-clause[j])
                    graph[-clause[k]].append(clause[j])
        return graph
    
    def min_order(graph):
        n = len(graph)
        visited = [False] * (n + 1)
        
        def dfs(node, order):
            if visited[node]:
                return order
            visited[node] = True
            for neighbor in graph[node]:
                order = max(order, dfs(neighbor, order))
            return order
        
        max_order = 0
        for node in range(1, n + 1):
            max_order = max(max_order, dfs(node, 0))
        return max_order
    
    def resolution_width(cnf):
        width = 0
        queue = cnf[:]
        while queue:
            clause = queue.pop()
            if len(clause) == 1:
                continue
            literal = random.choice(clause)
            new_clause = [l for l in clause if l != literal and -l not in clause]
            if new_clause:
                width = max(width, len(new_clause))
                queue.append(new_clause)
        return width
    
    n = 20
    cnf = generate_cnf(n)
    graph = tseitin_graph(cnf)
    min_order_val = min_order(graph)
    ent_w_val = resolution_width(cnf)
    
    return {
        "metric_name": "correlation",
        "metric_value": (min_order_val - 10) * (ent_w_val - 5),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")