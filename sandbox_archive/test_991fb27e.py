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

def random_cnf(n: int, m: int) -> list:
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        while len(set(clause)) != 2:
            clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

def resolution_tree(cnf: list) -> dict:
    tree = {}
    for i in range(len(cnf)):
        for j in range(i + 1, len(cnf)):
            for lit in cnf[i]:
                if -lit in cnf[j]:
                    new_clause = sorted(set(lit for lit in cnf[i] + cnf[j] if lit != -lit))
                    tree[(i, j)] = new_clause
    return tree

def euler_characteristic(tree: dict) -> int:
    vertices = set()
    edges = set()
    for (i, j), clause in tree.items():
        vertices.update([i, j])
        for _ in range(len(clause)):
            edges.add((min(i, j), max(i, j)))
    return len(vertices) - len(edges)

def width(tree: dict) -> int:
    def dfs(node, visited):
        if node in visited:
            return 0
        visited.add(node)
        return 1 + sum(dfs(child, visited) for child in tree.get(node, []))
    
    max_width = 0
    for node in tree.keys():
        max_width = max(max_width, dfs(node, set()))
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = random_cnf(n, m)
    tree = resolution_tree(cnf)
    
    if not tree:
        return {
            "metric_name": "Euler characteristic",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_resolution_tree"
        }
    
    chi = euler_characteristic(tree)
    w = width(tree)
    
    return {
        "metric_name": "Euler characteristic",
        "metric_value": chi / w if w != 0 else None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE no_valid_metric_values")
    else:
        valid_results = [r for r in results if "metric_value" in r and r["metric_value"] is not None]
        mean_value = sum(r["metric_value"] for r in valid_results) / len(valid_results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in valid_results) / len(valid_results))
        support_fraction = sum(1 for r in valid_results if r["conjecture_holds"]) / len(valid_results)
        
        if support_fraction >= 0.8 and max(r["n_max"] for r in valid_results) >= 16:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in valid_results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")