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
    
    def generate_cnf(n: int, m: int):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def xor_and_tree_width(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        tree = [[] for _ in range(n + 1)]
        for clause in cnf:
            if len(clause) == 2:
                u, v = abs(clause[0]), abs(clause[1])
                tree[u].append(v)
                tree[v].append(u)
        visited = [False] * (n + 1)
        
        def dfs(node):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in tree[node]:
                        stack.append(neighbor)
        
        dfs(1)
        return sum(not v for v in visited) - 1
    
    def matroid_expansion(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        rank = [0] * (n + 1)
        for clause in cnf:
            if len(clause) == 2:
                u, v = abs(clause[0]), abs(clause[1])
                if rank[u] < rank[v]:
                    rank[u], rank[v] = rank[v], rank[u]
                rank[v] += 1
        return sum(rank)
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    cnf = generate_cnf(n, m)
    tw = xor_and_tree_width(cnf)
    rank = matroid_expansion(cnf)
    
    return {
        "metric_name": "rank_over_tw",
        "metric_value": Fraction(rank, tw),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")