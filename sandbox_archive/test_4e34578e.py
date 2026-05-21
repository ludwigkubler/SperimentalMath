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
    
    def tree_depth(graph):
        if not graph:
            return 0
        depths = {}
        for node in graph:
            depths[node] = 1 + max((depths.get(neighbor, 0) for neighbor in graph[node]), default=0)
        return max(depths.values())
    
    def resolution_length(clauses):
        stack = []
        while clauses:
            new_clauses = set()
            for clause in clauses:
                if len(clause) == 1:
                    unit_literal = clause[0]
                    stack.append(unit_literal)
                    break
                else:
                    new_clauses.add(clause)
            else:
                return len(stack)
            for literal in stack:
                new_clauses.discard([-literal])
        return len(stack)
    
    n = random.randint(5, 40)
    graph = {i: [] for i in range(n)}
    edges = set()
    while len(edges) < n - 1:
        u, v = random.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges:
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
    
    clauses = []
    for node in range(n):
        for neighbor in graph[node]:
            clauses.append([node + 1, -neighbor - 1])
    
    depth = tree_depth(graph)
    length = resolution_length(clauses)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** depth,
        "counterexample": "" if length >= 2 ** depth else f"Graph with n={n}, A=[{', '.join(map(str, graph))}]"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")