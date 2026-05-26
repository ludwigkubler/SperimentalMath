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
    
    def tseitin_resolution_tree(clauses):
        n = len(clauses)
        tree = {}
        literals = set()
        
        for i in range(n):
            literals.add(i + 1)
            literals.add(-(i + 1))
        
        new_var = -1
        for clause in clauses:
            new_var -= 1
            tree[new_var] = []
            for lit in clause:
                if lit > 0:
                    tree[lit].append((new_var, 'not'))
                else:
                    tree[-lit].append((new_var, 'not'))
        
        return tree, literals
    
    def rank_of_tree(tree):
        visited = set()
        rank = 0
        
        def dfs(node):
            nonlocal rank
            if node in visited:
                return
            visited.add(node)
            for neighbor, _ in tree[node]:
                dfs(neighbor)
            rank += 1
        
        for node in tree:
            if node not in visited:
                dfs(node)
        
        return rank
    
    def depth_of_tree(tree):
        def dfs(node, current_depth):
            nonlocal max_depth
            if node in visited:
                return
            visited.add(node)
            max_depth = max(max_depth, current_depth)
            for neighbor, _ in tree[node]:
                dfs(neighbor, current_depth + 1)
        
        visited = set()
        max_depth = 0
        for node in tree:
            if node not in visited:
                dfs(node, 1)
        
        return max_depth
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([i + 1, -(i + 1)]) for i in range(random.randint(2, 3))]
        clauses.append(clause)
    
    tree, literals = tseitin_resolution_tree(clauses)
    rank = rank_of_tree(tree)
    depth = depth_of_tree(tree)
    
    metric_value = Fraction(rank, depth) if depth > 0 else float('inf')
    conjecture_holds = metric_value <= Fraction(1, 2)  # Placeholder constant c
    counterexample = "" if conjecture_holds else "unknown"
    
    return {
        "metric_name": "Rank/Depth Ratio",
        "metric_value": float(metric_value),
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"unknown\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_conjecture")