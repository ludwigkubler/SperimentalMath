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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tseitin_graph(cnf):
        literals = set()
        for clause in cnf:
            for literal in clause:
                literals.add(abs(literal))
        
        nodes = {0}
        edges = []
        
        for i, literal in enumerate(literals):
            nodes.add(i + 1)
            nodes.add(-i - 1)
            for j, other_literal in enumerate(literals):
                if j > i and (literal < 0 or other_literal < 0):
                    continue
                if literal * other_literal < 0:
                    edges.append((i + 1, -j - 1))
                    edges.append((-i - 1, j + 1))
        
        return nodes, edges
    
    def min_order(graph):
        nodes, edges = graph
        n = len(nodes)
        adj_matrix = [[0] * n for _ in range(n)]
        
        for u, v in edges:
            adj_matrix[u-1][v-1] = 1
            adj_matrix[v-1][u-1] = 1
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in range(n):
                        if adj_matrix[node][neighbor] and not visited[neighbor]:
                            stack.append(neighbor)
        
        visited = [False] * n
        dfs(0, visited)
        
        return sum(visited) - 1
    
    def resolution_width(cnf):
        clauses = cnf[:]
        width = 0
        
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(abs(lit) == abs(other_lit) and lit != other_lit for lit in clauses[i] for other_lit in clauses[j]):
                        new_clause = [lit for lit in clauses[i] if lit not in clauses[j]] + [other_lit for other_lit in clauses[j] if other_lit not in clauses[i]]
                        break
                if new_clause:
                    break
            if not new_clause:
                break
            clauses.append(new_clause)
            width += 1
        
        return width
    
    n = random.randint(5, 30)
    cnf = generate_cnf(n)
    graph = tseitin_graph(cnf)
    min_order_value = min_order(graph)
    ent_w_value = resolution_width(cnf)
    
    if min_order_value == 0 or ent_w_value == 0:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "min_order or ent_w is zero"
        }
    
    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        
        if std_x == 0 or std_y == 0:
            return [None]
        
        return [cov / (std_x * std_y)]
    
    correlation = pearson_correlation([min_order_value], [ent_w_value])[0]
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation is not None and abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 999983) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")