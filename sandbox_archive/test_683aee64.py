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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0 or d >= n:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for j in neighbors:
                if (i, j) not in edges_added and (j, i) not in edges_added:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
                    edges_added.add((i, j))
        return adj_matrix
    
    def is_connected(graph):
        n = len(graph)
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in range(n):
                    if graph[node][neighbor] == 1 and not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)
    
    def min_generators(graph):
        n = len(graph)
        generators = []
        for i in range(n):
            if sum(graph[i]) > 0:
                generators.append(i)
        return len(generators)
    
    def frege_proof_depth(graph):
        n = len(graph)
        if not is_connected(graph):
            return float('inf')
        
        def dpll(formula, assignment):
            if not formula:
                return True
            literal = next((lit for lit in range(1, 2 * n + 1) if lit not in assignment and -lit not in assignment), None)
            if literal is None:
                return False
            
            pos_lit = literal % 2 == 0
            new_assignment = assignment.copy()
            new_assignment[literal] = pos_lit
            
            clauses = [clause for clause in formula if (pos_lit and literal in clause) or (-pos_lit and -literal in clause)]
            if dpll(clauses, new_assignment):
                return True
            
            new_assignment[literal] = not pos_lit
            clauses = [clause for clause in formula if (-pos_lit and literal in clause) or (pos_lit and -literal in clause)]
            return dpll(clauses, new_assignment)
        
        formula = []
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 0:
                    formula.append([2 * i + 1, -(2 * j + 1)])
                    formula.append([-(2 * i + 1), 2 * j + 1])
        
        return len(formula)
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(d, n)
    if graph is None:
        return {
            "metric_name": "frege_proof_depth",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "graph_not_d_regular"
        }
    
    m_G = min_generators(graph)
    w_G = frege_proof_depth(graph)
    
    if w_G == float('inf'):
        return {
            "metric_name": "frege_proof_depth",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_connected"
        }
    
    expected = d ** 0.5 * n ** 0.75
    within_range = abs(m_G - expected) <= 0.1 * expected
    
    return {
        "metric_name": "frege_proof_depth",
        "metric_value": m_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": within_range,
        "counterexample": "" if within_range else f"m(G)={m_G}, expected={expected}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")