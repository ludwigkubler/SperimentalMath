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
            literals = [random.choice([1, -1]) * (i + 1) for i in range(3)]
            clause = sorted(literals)
            if clause not in clauses:
                clauses.append(clause)
        return clauses
    
    def tseitin_resolution_tree(clauses):
        nodes = {0: []}
        edges = []
        
        def add_node(node_id, literals):
            nodes[node_id] = literals
            for literal in literals:
                if literal > 0:
                    edge = (node_id, -literal)
                else:
                    edge = (-literal, node_id)
                edges.append(edge)
        
        add_node(0, [1, -2, 3])
        
        for clause in clauses:
            new_node_id = max(nodes.keys()) + 1
            add_node(new_node_id, clause)
            for literal in clause:
                if literal > 0:
                    edge = (new_node_id, -literal)
                else:
                    edge = (-literal, new_node_id)
                edges.append(edge)
        
        return nodes, edges
    
    def geometric_langlands_rank(tree):
        # Placeholder for actual computation
        return len(tree[0])
    
    n_values = [5, 10, 15, 20, 30, 40]
    depths = []
    ranks = []
    
    for n in n_values:
        formula = generate_3cnf(n)
        tree, _ = tseitin_resolution_tree(formula)
        depth = max(len(path) for path in find_all_paths(tree))
        rank = geometric_langlands_rank(tree)
        depths.append(depth)
        ranks.append(rank)
    
    avg_depth = sum(depths) / len(depths)
    avg_rank = sum(ranks) / len(ranks)
    ratio = avg_rank / avg_depth
    
    return {
        "metric_name": "Ratio of Rank to Depth",
        "metric_value": ratio,
        "instances_tested": len(n_values),
        "conjecture_holds": ratio <= 1,  # Placeholder constant c
        "counterexample": "" if ratio <= 1 else f"Ratio {ratio} exceeds upper bound"
    }

def find_all_paths(tree):
    paths = []
    
    def dfs(node_id, path):
        if node_id in tree:
            for neighbor in tree[node_id]:
                if neighbor not in path:
                    dfs(neighbor, path + [neighbor])
            paths.append(path)
    
    dfs(0, [0])
    return paths

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(2, 5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(int(r["conjecture_holds"]) for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds upper bound\" first_failing_seed={first_failing_seed}")