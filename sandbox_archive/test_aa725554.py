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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or n < d + 1:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(1, 2 * n + 1)]
        clauses = []
        
        for i in range(n):
            if not graph[i]:
                continue
            clause = [-literals[2 * i - 1]]
            for j in graph[i]:
                clause.append(literals[2 * j])
            clauses.append(clause)
            
            for j in graph[i]:
                for k in graph[j]:
                    if k != i:
                        clause = [literals[2 * i], literals[2 * j + 1], literals[2 * k + 1]]
                        clauses.append(clause)
        
        return clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        learned_clauses = []
        width = 0
        
        while queue:
            clause = queue.pop(0)
            if len(clause) > width:
                width = len(clause)
            
            for learned_clause in learned_clauses:
                resolvents = set()
                for l in learned_clause:
                    if -l in clause:
                        new_clause = [x for x in learned_clause + clause if x != -l and x != l]
                        resolvents.add(tuple(sorted(new_clause)))
                queue.extend(resolvents)
                learned_clauses.extend(resolvents)
        
        return width
    
    def diophantine_equations(graph):
        n = len(graph)
        equations = set()
        
        for i in range(n):
            if not graph[i]:
                continue
            for j in graph[i]:
                a, b = random.randint(1, 10), random.randint(1, 10)
                c = a * j + b * i
                equation = (a, b, c)
                equations.add(equation)
        
        return equations
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)
        if not graph:
            continue
        
        equations = diophantine_equations(graph)
        width = resolution_width(tseitin_formula(graph))
        
        results.append({
            "n": n,
            "equations": len(equations),
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graph generated"
        }
    
    x = [result["equations"] for result in results]
    y = [result["width"] for result in results]
    correlation = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation >= 0.8 and all(correlation >= 0.7 for result in results),
        "counterexample": "" if correlation >= 0.8 else f"Correlation < 0.7: {correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(not r["conjecture_holds"] for r in results and r["metric_value"] < 0.7 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation < 0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_support")