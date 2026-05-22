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
    
    def is_k_clique(G, k):
        n = len(G)
        for nodes in itertools.combinations(range(n), k):
            if not all(G[i][j] == 1 for i, j in itertools.combinations(nodes, 2)):
                return False
        return True
    
    def symmetry_group_order(G):
        n = len(G)
        generators = []
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 0:
                    continue
                generator = [(i, j)]
                visited = set([i, j])
                while True:
                    new_nodes = [node for node in range(n) if node not in visited and any(G[node][v] == 1 for v in visited)]
                    if not new_nodes:
                        break
                    next_node = random.choice(new_nodes)
                    generator.append(next_node)
                    visited.add(next_node)
                generators.append(generator)
        return len(generators)
    
    n = random.randint(5, 40)
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    if is_k_clique(G, k=3):
        return {
            "metric_name": "symmetry_group_order",
            "metric_value": symmetry_group_order(G),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k-CLIQUE graph"
        }
    
    if symmetry_group_order(G) < n**0.25:
        return {
            "metric_name": "symmetry_group_order",
            "metric_value": symmetry_group_order(G),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Non-k-CLIQUE graph with order < Θ(n^{0.25})"
        }
    
    return {
        "metric_name": "symmetry_group_order",
        "metric_value": symmetry_group_order(G),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "k-CLIQUE graph" for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"] == "k-CLIQUE graph")
        print(f"RESULT: FALSIFIED counterexample=\"k-CLIQUE graph\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")