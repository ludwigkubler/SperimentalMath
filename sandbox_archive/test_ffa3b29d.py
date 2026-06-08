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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or d < 1 or d >= n:
            return None
        adj_list = [[] for _ in range(n)]
        edges_added = set()
        for i in range(d):
            for j in range(i + 1, n):
                if len(adj_list[i]) == d and len(adj_list[j]) == d:
                    continue
                if (i, j) not in edges_added and (j, i) not in edges_added:
                    adj_list[i].append(j)
                    adj_list[j].append(i)
                    edges_added.add((i, j))
        return adj_list
    
    def tseitin_formula(adj_list):
        n = len(adj_list)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in adj_list[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
            for j in range(i + 1, n):
                if i not in adj_list[j] and j not in adj_list[i]:
                    clause = [-literals[i], -literals[j]]
                    clauses.append(clause)
        return literals, clauses
    
    def dpll(literals, clauses):
        assignment = {}
        stack = []
        
        def solve():
            while True:
                if not stack:
                    if all(c in assignment for c in clauses):
                        return assignment
                    unit_clause = next((c for c in clauses if len(c) == 1), None)
                    if unit_clause is None:
                        return None
                    literal = unit_clause[0]
                    assignment[literal] = True
                else:
                    literal, negated = stack.pop()
                    if negated:
                        assignment[literal] = False
                    else:
                        assignment[literal] = True
                        for clause in clauses:
                            if literal in clause:
                                clause.remove(literal)
                                if not clause:
                                    return None
    
    def minimal_tropical_motivic_rank(adj_list):
        n = len(adj_list)
        rank = 0
        visited = [False] * n
        
        def dfs(node, parent):
            nonlocal rank
            rank += 1
            for neighbor in adj_list[node]:
                if neighbor != parent and not visited[neighbor]:
                    visited[neighbor] = True
                    dfs(neighbor, node)
        
        for i in range(n):
            if not visited[i]:
                visited[i] = True
                dfs(i, -1)
        
        return rank
    
    def resolution_proof_width(literals, clauses):
        n = len(literals)
        assignment = {}
        stack = []
        
        def solve():
            while True:
                if not stack:
                    if all(c in assignment for c in clauses):
                        return 0
                    unit_clause = next((c for c in clauses if len(c) == 1), None)
                    if unit_clause is None:
                        return None
                    literal = unit_clause[0]
                    assignment[literal] = True
                else:
                    literal, negated = stack.pop()
                    if negated:
                        assignment[literal] = False
                    else:
                        assignment[literal] = True
                        for clause in clauses:
                            if literal in clause:
                                clause.remove(literal)
                                if not clause:
                                    return None
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "mtr(G)/w(φ_G)",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "d-regular graph generation failed"
        }
    
    literals, clauses = tseitin_formula(graph)
    mtr_G = minimal_tropical_motivic_rank(graph)
    w_phi_G = resolution_proof_width(literals, clauses)
    
    if w_phi_G == 0:
        return {
            "metric_name": "mtr(G)/w(φ_G)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution proof width is zero"
        }
    
    ratio = mtr_G / w_phi_G
    return {
        "metric_name": "mtr(G)/w(φ_G)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")