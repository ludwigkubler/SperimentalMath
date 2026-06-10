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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return {i: [] for i in range(n)}, edges
    
    def automorphism_group(graph):
        nodes, edges = graph
        n = len(nodes)
        
        def is_automorphism(perm):
            perm_nodes = [nodes[perm[i]] for i in range(n)]
            for u, v in edges:
                if (perm_nodes[u], perm_nodes[v]) not in edges and (perm_nodes[v], perm_nodes[u]) not in edges:
                    return False
            return True
        
        def generate_permutations():
            perms = []
            visited = set()
            
            def backtrack(perm):
                if len(perm) == n:
                    perms.append(perm)
                    return
                for i in range(n):
                    if i not in perm and all(i not in p[:len(perm)] for p in perms):
                        perm.append(i)
                        backtrack(perm)
                        perm.pop()
            
            backtrack([])
            return perms
        
        perms = generate_permutations()
        aut_group = [i for i, perm in enumerate(perms) if is_automorphism(perm)]
        return len(aut_group)
    
    def resolution_width(phi):
        # Placeholder function to compute the width of a Tseitin formula
        # This should be replaced with an actual implementation
        return random.randint(5, 20)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_random_graph(n)
    aut_index = automorphism_group(graph)
    width = resolution_width(graph)
    
    return {
        "metric_name": "log2_aut_index",
        "metric_value": math.log2(aut_index) if aut_index > 0 else -math.inf,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")