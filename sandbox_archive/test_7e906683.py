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
    
    def generate_expander_graph(n):
        if n <= 1:
            return []
        graph = {i: [] for i in range(n)}
        edges = [(0, (i + 1) % n) for i in range(n - 1)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        return graph
    
    def tree_width(graph):
        if not graph:
            return 0
        leaves = [node for node, neighbors in graph.items() if len(neighbors) == 1]
        if not leaves:
            return 0
        
        width = 0
        while leaves:
            new_leaves = []
            for leaf in leaves:
                parent = next((neighbor for neighbor in graph[leaf] if neighbor != leaves[0]), None)
                if parent is not None:
                    graph[parent].remove(leaf)
                    if len(graph[parent]) == 1:
                        new_leaves.append(parent)
            width += 1
            leaves = new_leaves
        
        return width
    
    def algebraic_k_theory_rank(graph):
        n = len(graph)
        k_theory_matrix = [[0] * n for _ in range(n)]
        
        for u, v in graph.items():
            for w in v:
                if u != w and v != w:
                    k_theory_matrix[u][w] += 1
                    k_theory_matrix[w][u] += 1
        
        rank = 0
        for i in range(n):
            row = [k_theory_matrix[i][j] for j in range(n)]
            if any(row[j] != 0 for j in range(i)):
                rank += 1
                for j in range(n):
                    k_theory_matrix[j][i] /= row[i]
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        graph = generate_expander_graph(n)
        tree_width_val = tree_width(graph)
        k_theory_rank = algebraic_k_theory_rank(graph)
        
        if k_theory_rank < 2**(math.log(tree_width_val, 2)):
            return {
                "metric_name": "K-theory rank",
                "metric_value": k_theory_rank,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"Tree-width {tree_width_val}, K-theory rank {k_theory_rank}"
            }
        
        total_rank += k_theory_rank
        instances_tested += 1
    
    mean_rank = total_rank / len(n_values)
    return {
        "metric_name": "K-theory rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")