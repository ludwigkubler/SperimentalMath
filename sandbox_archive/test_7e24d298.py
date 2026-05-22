# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def resolution_graph(cnf):
        graph = {}
        for i in range(len(cnf)):
            for j in range(i + 1, len(cnf)):
                if any(abs(x) == abs(y) and x * y < 0 for x in cnf[i] for y in cnf[j]):
                    for var in set(cnf[i]) | set(cnf[j]):
                        if var not in graph:
                            graph[var] = []
                        if -var not in graph:
                            graph[-var] = []
                        if j not in graph[var]:
                            graph[var].append(j)
                        if i not in graph[-var]:
                            graph[-var].append(i)
        return graph
    
    def minimal_rank(graph):
        rank = 0
        visited = set()
        for node in graph:
            if node not in visited:
                queue = [node]
                while queue:
                    current = queue.pop(0)
                    if current not in visited:
                        visited.add(current)
                        for neighbor in graph[current]:
                            if neighbor not in visited:
                                queue.append(neighbor)
                rank += 1
        return rank
    
    def monotone_circuit_depth(cnf):
        n = len(cnf)
        graph = resolution_graph(cnf)
        
        def dfs(node, parent):
            nonlocal depth
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor != parent:
                        dfs(neighbor, node)
                depth = max(depth, len(visited))
        
        visited = set()
        depth = 0
        for i in range(n):
            dfs(i, None)
        return depth
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph = resolution_graph(cnf)
    rank = minimal_rank(graph)
    depth = monotone_circuit_depth(cnf)
    
    if rank > depth:
        return {
            "metric_name": "Rank vs Depth",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CNF with n={n} has rank {rank} and depth {depth}"
        }
    
    return {
        "metric_name": "Rank vs Depth",
        "metric_value": abs(rank - depth),
        "instances_tested": 1,
        "conjecture_holds": abs(rank - depth) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100))[:30]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = min((result["counterexample"] for result in results if not result["conjecture_holds"]), default="")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")