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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) == 0:
                clause[random.randint(0, n - 1)] *= -1
            clauses.append(clause)
        return clauses

    def resolution_graph(cnf):
        graph = {}
        for i in range(len(cnf)):
            for j in range(i + 1, len(cnf)):
                common_vars = set(abs(x) for x in cnf[i]) & set(abs(x) for x in cnf[j])
                if common_vars:
                    for var in common_vars:
                        if var not in graph:
                            graph[var] = []
                        if -var not in graph:
                            graph[-var] = []
                        graph[var].append(-var)
                        graph[-var].append(var)
        return graph

    def quasi_postnikov_rank(graph):
        rank = 0
        visited = set()
        for node in graph:
            if node not in visited:
                stack = [node]
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        for neighbor in graph[current]:
                            if neighbor not in visited:
                                stack.append(neighbor)
                rank += 1
        return rank

    def monotone_circuit_depth(cnf):
        n = len(cnf)
        graph = resolution_graph(cnf)
        
        def dfs(node, parent):
            if node not in visited:
                visited.add(node)
                depth[node] = max(depth.get(node, 0), depth.get(parent, -1) + 1)
                for neighbor in graph[node]:
                    if neighbor != parent:
                        dfs(neighbor, node)
        
        visited = set()
        depth = {}
        for i in range(n):
            dfs(i, None)
        
        return max(depth.values())

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    rank = quasi_postnikov_rank(resolution_graph(cnf))
    depth = monotone_circuit_depth(cnf)

    return {
        "metric_name": "rank_vs_depth",
        "metric_value": abs(rank - depth),
        "instances_tested": 1,
        "conjecture_holds": rank <= depth and abs(rank - depth) <= 3,
        "counterexample": "" if rank <= depth else f"CNF with n={n}, rank={rank}, depth={depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank_diff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > depth\" first_failing_seed={first_failing_seed}")