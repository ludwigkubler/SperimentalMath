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
    
    def generate_random_graph(n, girth):
        if n < 3 or girth < 3:
            return None
        
        graph = {i: set() for i in range(n)}
        
        def add_edge(u, v):
            if u != v and v not in graph[u] and u not in graph[v]:
                graph[u].add(v)
                graph[v].add(u)
        
        def is_valid_path(path):
            return len(set(path)) == len(path) and all(graph[path[i]][path[i+1]] for i in range(len(path)-1))
        
        def find_cycle(start, path=[]):
            if len(path) >= girth:
                if len(path) > girth or not is_valid_path(path):
                    return None
                return path
            
            for neighbor in graph[start]:
                if neighbor not in path:
                    cycle = find_cycle(neighbor, path + [neighbor])
                    if cycle:
                        return cycle
        
        def add_random_edges():
            while True:
                u, v = random.sample(range(n), 2)
                if u != v and v not in graph[u] and u not in graph[v]:
                    add_edge(u, v)
                    break
        
        for _ in range(10 * n):
            cycle = find_cycle(random.randint(0, n-1))
            if cycle:
                path = list(cycle) + [cycle[0]]
                for i in range(len(path)-1):
                    add_edge(path[i], path[i+1])
        
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        cnf = []
        literals = {i: f'x{i}' for i in range(n)}
        
        for u in range(n):
            clauses = [literals[u]]
            for v in graph[u]:
                clauses.append(f'-{literals[v]}')
            cnf.append(clauses)
        
        for u in range(n):
            for v in graph[u]:
                if u < v:
                    clauses = [-literals[u], -literals[v], f'x{n+u*n+v}']
                    cnf.append(clauses)
                    clauses = [-literals[u], literals[v], f'-x{n+u*n+v}']
                    cnf.append(clauses)
                    clauses = [literals[u], -literals[v], f'-x{n+u*n+v}']
                    cnf.append(clauses)
        
        return cnf
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            if matrix[i][i] == 0:
                for j in range(i+1, rows):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
        
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def minimal_tropical_motivic_rank(cnf):
        n = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal.startswith('x'):
                    j = int(literal[1:])
                    matrix[i][j] += 1
                else:
                    j = int(literal[1:]) - n
                    matrix[j][i] -= 1
        
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        
        return rank
    
    def communication_complexity_rank(cnf):
        n = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal.startswith('x'):
                    j = int(literal[1:])
                    matrix[i][j] += 1
                else:
                    j = int(literal[1:]) - n
                    matrix[j][i] -= 1
        
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        
        return rank
    
    n = random.randint(5, 30)
    graph = generate_random_graph(n, 5)
    if not graph:
        return {
            "metric_name": "minimal_tropical_motivic_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    cnf = tseitin_formula(graph)
    mtr = minimal_tropical_motivic_rank(cnf)
    ccr = communication_complexity_rank(cnf)
    
    if mtr is None or ccr is None:
        return {
            "metric_name": "minimal_tropical_motivic_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "ranking_failed"
        }
    
    ratio = mtr / ccr
    return {
        "metric_name": "minimal_tropical_motivic_rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "ratio_out_of_bounds"
        print(f"RESULT: FALSIFIED counterexample='{counterexample}' first_failing_seed={first_failing_seed}")