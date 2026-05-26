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
    
    def generate_tseitin_tree(w, h):
        if w <= 0 or h <= 0:
            return None
        tree = {}
        for i in range(h):
            level = []
            for j in range(w):
                node = (i, j)
                level.append(node)
                if i > 0:
                    parent = (i-1, j)
                    tree[node] = parent
            tree[level[0]] = None
        return tree
    
    def deligne_lusztig_cone(tree):
        if not tree:
            return 0
        nodes = list(tree.keys())
        n = len(nodes)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i, node1 in enumerate(nodes):
            parent1 = tree[node1]
            if parent1 is not None:
                j = nodes.index(parent1)
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
        rank = gaussian_elimination(adjacency_matrix)
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i+1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return n - i - 1
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return n - sum(1 for row in matrix if all(x == 0 for x in row))
    
    def min_rank(tree):
        nodes = list(tree.keys())
        ranks = []
        for node in nodes:
            sub_tree = {n: p for n, p in tree.items() if n != node}
            rank = deligne_lusztig_cone(sub_tree)
            ranks.append(rank)
        return min(ranks)
    
    def tseitin_resolution_tree_width(tree):
        max_width = 0
        for level in range(len(tree)):
            width = sum(1 for node, parent in tree.items() if parent is not None and parent[0] == level)
            max_width = max(max_width, width)
        return max_width
    
    def tseitin_resolution_tree_height(tree):
        height = 0
        for node, parent in tree.items():
            if parent is None:
                continue
            current_node = parent
            current_height = 1
            while current_node is not None:
                current_node = tree[current_node]
                current_height += 1
            height = max(height, current_height)
        return height
    
    n = random.randint(5, 40)
    w = random.randint(2, n)
    h = random.randint(2, n)
    tree = generate_tseitin_tree(w, h)
    
    if not tree:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rho = min_rank(tree)
    w2_over_h = (w ** 2) / h
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rho,
        "instances_tested": 1,
        "conjecture_holds": min_rho <= w2_over_h,
        "counterexample": "" if min_rho <= w2_over_h else f"min_rho={min_rho}, w^2/h={w2_over_h}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={results[0]['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")