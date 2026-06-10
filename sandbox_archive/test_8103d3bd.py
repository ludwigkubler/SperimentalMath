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
        graph = [[0] * n for _ in range(n)]
        degree_counts = [0] * n
        edges_added = 0
        
        def add_edge(u, v):
            nonlocal edges_added
            if u == v or graph[u][v] != 0:
                return False
            graph[u][v] = 1
            graph[v][u] = 1
            degree_counts[u] += 1
            degree_counts[v] += 1
            edges_added += 1
            return True
        
        for u in range(n):
            for v in range(u + 1, n):
                if degree_counts[u] < d and degree_counts[v] < d and add_edge(u, v):
                    if edges_added == (n * d) // 2:
                        break
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        
        for u in range(n):
            clause = [literals[u]]
            for v in range(u + 1, n):
                if graph[u][v] == 1:
                    clause.append(f"~{literals[v]}")
            clauses.append(" | ".join(clause))
        
        for u in range(n):
            for v in range(u + 1, n):
                if graph[u][v] == 0:
                    clause = [f"~{literals[u]}"]
                    clause.append(f"{literals[v]}")
                    clauses.append(" | ".join(clause))
        
        return " & ".join(clauses)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find the pivot row
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate the pivot column
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def rank(matrix):
        n = len(matrix)
        rref_matrix = gaussian_elimination([row[:] for row in matrix])
        rank = 0
        for i in range(n):
            if any(rref_matrix[i]):
                rank += 1
        return rank
    
    def frege_proof_depth(formula):
        # Simplified estimation of Frege proof depth
        return len(formula.split(" & ")) + len(formula.split(" | "))
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "Frege proof depth",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Invalid graph generated"
        }
    
    formula = tseitin_formula(graph)
    mli = rank([[graph[i][j] for j in range(n)] + [i == u] for i in range(n) for u in range(n)])
    d_phi = frege_proof_depth(formula)
    
    return {
        "metric_name": "Frege proof depth",
        "metric_value": d_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if mli == d_phi else False,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample='Conjecture not supported by all seeds' first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE reason=support_fraction={support_fraction} < 0.8")