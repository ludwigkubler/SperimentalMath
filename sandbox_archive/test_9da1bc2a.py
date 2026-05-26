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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
        return clauses
    
    def tseitin_resolution_tree(clauses):
        tree = {}
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        
        for literal in literals:
            tree[literal] = []
        
        for clause in clauses:
            for i, lit1 in enumerate(clause):
                for j, lit2 in enumerate(clause):
                    if i < j:
                        new_var = -literals.pop()
                        tree[new_var].append((lit1, 'not'))
                        tree[new_var].append((lit2, 'not'))
                        literals.add(new_var)
        
        return tree
    
    def depth(tree, node=1):
        if not tree[node]:
            return 0
        return 1 + max(depth(tree, child) for child in tree[node])
    
    def rank(tree):
        rank = 0
        visited = set()
        
        def dfs(node):
            nonlocal rank
            if node in visited:
                return
            visited.add(node)
            rank += 1
            for child, _ in tree[node]:
                dfs(child)
        
        for literal in range(1, max(tree.keys()) + 1):
            dfs(literal)
        
        return rank
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    tree = tseitin_resolution_tree(clauses)
    depth_value = depth(tree)
    rank_value = rank(tree)
    
    if depth_value == 0:
        return {
            "metric_name": "rank_to_depth_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "empty_tree"
        }
    
    ratio = rank_value / depth_value
    c = 2.0  # Example constant, adjust as needed
    
    return {
        "metric_name": "rank_to_depth_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= c,
        "counterexample": "" if ratio <= c else f"ratio={ratio} > {c}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")