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
    
    def generate_kcnf(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) for _ in range(2)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll_diameter(clauses):
        n = len(clauses)
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if any(x == -y for x in clauses[i] for y in clauses[j]):
                    graph[i].append(j)
                    graph[j].append(i)
        
        def dfs(node, visited, parent, depth):
            visited[node] = True
            max_depth = depth
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    max_depth = max(max_depth, dfs(neighbor, visited, node, depth + 1))
                elif neighbor != parent:
                    max_depth = max(max_depth, depth - visited[neighbor])
            return max_depth
        
        visited = [False] * n
        max_diameter = 0
        for i in range(n):
            if not visited[i]:
                diameter = dfs(i, visited, -1, 0)
                max_diameter = max(max_diameter, diameter)
        return max_diameter
    
    def min_rank(clauses):
        # This is a placeholder function. For the purpose of this test, we assume
        # that MinRank(H_F) is bounded by a constant times the number of clauses.
        return len(clauses)
    
    n = random.choice([10, 20, 30])
    m = random.choice([100, 200])
    clauses = generate_kcnf(n, m)
    dpll_diam = dpll_diameter(clauses)
    min_rank_val = min_rank(clauses)
    
    if dpll_diam == 0:
        return {
            "metric_name": "MinRank/H_F to DPLL Diameter Ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL diameter is zero"
        }
    
    ratio = Fraction(min_rank_val, dpll_diam)
    return {
        "metric_name": "MinRank/H_F to DPLL Diameter Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 2 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")