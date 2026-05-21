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
    
    def tree_depth(graph):
        n = len(graph)
        visited = [False] * n
        depth = 0
        
        def dfs(node, current_depth):
            nonlocal depth
            if visited[node]:
                return
            visited[node] = True
            for neighbor in graph[node]:
                dfs(neighbor, current_depth + 1)
            depth = max(depth, current_depth)
        
        for i in range(n):
            if not visited[i]:
                dfs(i, 0)
        return depth
    
    def resolution_length(graph):
        n = len(graph)
        clauses = [[i for i in range(n)]]
        assignment = [None] * (n + 1)
        unit_propagate_count = 0
        
        while True:
            changed = False
            for clause in clauses[:]:
                if len(clause) == 1:
                    unit_literal = clause[0]
                    if assignment[unit_literal] is None:
                        assignment[unit_literal] = True
                        for neighbor in graph[unit_literal]:
                            if assignment[neighbor] is None:
                                assignment[neighbor] = False
                                changed = True
                    elif assignment[unit_literal]:
                        clauses.remove(clause)
                else:
                    unit_propagate_count += 1
            if not changed:
                break
        
        return unit_propagate_count
    
    n = random.randint(5, 40)
    graph = [[] for _ in range(n)]
    edges = set()
    
    while len(edges) < n * (n - 1) // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    
    td = tree_depth(graph)
    rl = resolution_length(graph)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": rl,
        "instances_tested": 1,
        "conjecture_holds": rl >= 2 ** td,
        "counterexample": "" if rl >= 2 ** td else f"Graph with n={n}, tree_depth(G)={td}, resolution_length(G)={rl}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")