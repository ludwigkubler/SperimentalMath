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
        graph = {i: [] for i in range(n)}
        for _ in range(d * n // 2):
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
        return graph

    def calculate_mli(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i, neighbors in enumerate(graph):
            for j in neighbors:
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for col in range(cols):
                pivot_row = -1
                for row in range(rank, rows):
                    if matrix[row][col] != 0:
                        pivot_row = row
                        break
                if pivot_row == -1:
                    continue
                
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                
                for row in range(rank, rows):
                    factor = matrix[row][col]
                    for j in range(cols):
                        matrix[row][j] -= factor * matrix[pivot_row][j]
            return rank
        
        mli = n - gaussian_elimination(adjacency_matrix)
        return mli

    def resolution_proof_width(graph):
        n = len(graph)
        clauses = []
        
        for u, neighbors in graph.items():
            clause = [f'x{u}']
            for v in neighbors:
                clause.append(f'-x{v}')
            clauses.append(clause)
        
        def resolve(clauses):
            new_clauses = []
            while True:
                added_clause = False
                for i in range(len(clauses)):
                    for j in range(i + 1, len(clauses)):
                        p, q = clauses[i], clauses[j]
                        if any(x == f'-{y}' for x in p for y in q):
                            new_clause = [x for x in p if x not in q and x[0] != '-'] + \
                                          [f'-{y}' for y in q if y not in p and y[0] != '-']
                            new_clauses.append(new_clause)
                            added_clause = True
                if not added_clause:
                    break
            return new_clauses
        
        while len(clauses) > 1:
            clauses = resolve(clauses)
        
        return len(clauses[0])

    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    
    mli = calculate_mli(graph)
    w_phi_G = resolution_proof_width(graph)
    
    return {
        "metric_name": "mli(G)",
        "metric_value": mli,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mli <= w_phi_G,
        "counterexample": "" if mli <= w_phi_G else f"mli(G)={mli}, w(φ_G)={w_phi_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean_metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r)
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_counterexamples_found")