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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def term_graph(cnf):
        graph = {}
        for clause in cnf:
            for literal in clause:
                if literal not in graph:
                    graph[literal] = set()
                for other_literal in clause:
                    if other_literal != literal and -literal not in clause:
                        graph[literal].add(other_literal)
                        graph[other_literal].add(literal)
        return graph
    
    def minimal_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * (2 * n + 1)
        
        def dfs(node, color):
            if visited[node]:
                return True
            visited[node] = True
            for neighbor in graph[node]:
                if neighbor != -node and not dfs(neighbor, 3 - color):
                    return False
            return True
        
        for i in range(1, n + 1):
            if not visited[i] and not dfs(i, 1):
                rank += 1
        return rank
    
    def resolution_width(cnf):
        clauses = set()
        for clause in cnf:
            clauses.add(tuple(sorted(clause)))
        
        queue = list(clauses)
        while queue:
            new_clauses = []
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                        if new_clause not in clauses and new_clause not in new_clauses:
                            new_clauses.append(new_clause)
            queue.extend(new_clauses)
        
        return len(queue)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph = term_graph(cnf)
    mrank = minimal_rank(graph)
    w_phi = resolution_width(cnf)
    
    if w_phi == 0:
        return {
            "metric_name": "mrank/w_phi",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    ratio = mrank / w_phi
    return {
        "metric_name": "mrank/w_phi",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 2) < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"RESULT: FALSIFIED counterexample='mrank/w_phi' first_failing_seed={first_failing_seed}"
    
    print(result)