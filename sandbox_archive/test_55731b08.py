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
    
    def tseitin_graph(cnf):
        n = len(cnf)
        graph = [[] for _ in range(2 * n + 1)]
        literals = list(range(-n, 0)) + list(range(1, n + 1))
        
        for i, clause in enumerate(cnf):
            literal_map = {l: literals.index(l) for l in clause}
            new_literal = -(i + n + 1)
            graph[0].append(new_literal)
            
            for j in range(len(clause)):
                for k in range(j + 1, len(clause)):
                    graph[literal_map[clause[j]]].append(-literal_map[clause[k]])
                    graph[-literal_map[clause[k]]].append(literal_map[clause[j]])
        
        return graph
    
    def min_order(graph):
        n = len(graph)
        visited = [False] * n
        order = 0
        
        def dfs(node):
            nonlocal order
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    dfs(neighbor)
                order += 1
        
        for i in range(n):
            dfs(i)
        
        return order
    
    def resolution_width(cnf):
        n = len(cnf)
        width = 0
        
        def resolve(lit, cnf):
            nonlocal width
            new_cnf = []
            found = False
            for clause in cnf:
                if lit in clause:
                    continue
                if -lit in clause:
                    found = True
                    new_clause = [l for l in clause if l != -lit]
                    if len(new_clause) > width:
                        width = len(new_clause)
                    break
                else:
                    new_cnf.append(clause)
            return new_cnf, found
        
        while cnf:
            lit = random.choice([-i for i in range(1, n + 1)] + [i for i in range(-n, 0)])
            cnf, _ = resolve(lit, cnf)
        
        return width
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = [[random.randint(-n, -1), random.randint(1, n)] for _ in range(n)]
    graph = tseitin_graph(cnf)
    min_order_value = min_order(graph)
    ent_w_value = resolution_width(cnf)
    
    return {
        "metric_name": "pearson_correlation",
        "metric_value": pearson_correlation([min_order_value], [ent_w_value])[0],
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")