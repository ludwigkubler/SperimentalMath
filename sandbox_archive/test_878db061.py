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
        for _ in range(10 * n):  # 10 clauses per variable on average
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause.reverse()
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = []
        while cnf:
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if not unit_clause:
                return -1
            literal = unit_clause[0]
            cnf.remove(unit_clause)
            new_clauses = [c for c in cnf if literal not in c and -literal not in c]
            cnf.extend(new_clauses)
            stack.append(literal)
        return len(stack)
    
    def term_graph(cnf):
        graph = {}
        for clause in cnf:
            for lit1, lit2 in itertools.combinations(clause, 2):
                if abs(lit1) != abs(lit2):
                    u, v = sorted([abs(lit1), abs(lit2)])
                    if u not in graph:
                        graph[u] = []
                    if v not in graph:
                        graph[v] = []
                    graph[u].append(v)
                    graph[v].append(u)
        return graph
    
    def minimal_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * (n + 1)
        
        def dfs(node, color):
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    if visited[neighbor] and color == visited[neighbor]:
                        return False
                    elif not visited[neighbor]:
                        if not dfs(neighbor, -color):
                            return False
                return True
        
        for i in range(1, n + 1):
            if not visited[i]:
                if not dfs(i, 1):
                    rank += 1
        return rank
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                matrix[i][j] /= matrix[i][i]
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    for k in range(i + 1, n):
                        matrix[j][k] -= matrix[i][k] * matrix[j][i]
        return matrix
    
    def rank(matrix):
        reduced_matrix = gaussian_elimination(matrix)
        if reduced_matrix is None:
            return math.inf
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank
    
    n = 20
    cnf = generate_cnf(n)
    graph = term_graph(cnf)
    mrank = minimal_rank(graph)
    w_phi = resolution_width(cnf)
    
    if w_phi == -1:
        return {
            "metric_name": "mrank_w_ratio",
            "metric_value": math.inf,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_unbounded"
        }
    
    mrank_w_ratio = abs(mrank) / abs(w_phi)
    return {
        "metric_name": "mrank_w_ratio",
        "metric_value": mrank_w_ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mrank_w_ratio <= 2 and mrank_w_ratio >= 0.5,
        "counterexample": ""
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
        counterexample = "mrank_w_ratio_out_of_bounds"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")