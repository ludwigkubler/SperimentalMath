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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def generate_d_regular_graph(d, n):
        if (d * n) % 2 != 0 or d >= n:
            raise ValueError("Invalid parameters for generating a d-regular graph")
        
        G = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            while any(j in edges for j in neighbors) or any(i in edges for j in neighbors):
                neighbors = random.sample(range(n), d)
            for j in neighbors:
                if (i, j) not in edges and (j, i) not in edges:
                    G[i].append(j)
                    G[j].append(i)
                    edges.add((i, j))
        return G

    def tseitin_formula(G):
        n = len(G)
        literals = {i: f'x{i}' for i in range(n)}
        neg_literals = {i: f'-x{i}' for i in range(n)}
        
        clauses = []
        for i in range(n):
            clause = [neg_literals[i]]
            for j in G[i]:
                clause.append(literals[j])
            clauses.append(clause)
            
            for j in G[i]:
                for k in G[j]:
                    if k != i:
                        clause = [neg_literals[i], neg_literals[j], literals[k]]
                        clauses.append(clause)
        
        return clauses

    def gaussian_elimination(A, b):
        n = len(A)
        M = A + [b]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            
            factor = M[i][i]
            for j in range(n + 1):
                M[i][j] /= factor
            
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(n + 1):
                        M[j][k] -= factor * M[i][k]
        
        return [M[i][-1] for i in range(n)]

    def resolution_width(clauses):
        n = len(clauses)
        clauses = [[-l if l < 0 else l for l in c] for c in clauses]
        unit_clauses = {c[0]: -c[0] for c in clauses if len(c) == 1}
        
        def resolve(l, m):
            return [x for x in l + m if x != -m and x != l]
        
        queue = list(unit_clauses.keys())
        while queue:
            l = queue.pop(0)
            for i, m in enumerate(clauses):
                if l in m:
                    new_clause = resolve(l, m)
                    if len(new_clause) == 1:
                        unit_clauses[new_clause[0]] = -new_clause[0]
                        queue.append(new_clause[0])
                    else:
                        clauses[i] = new_clause
        return max(len(c) for c in clauses)

    def kostant_multi_index(clauses):
        n = len(clauses)
        A = [[0] * (n + 1) for _ in range(n)]
        b = [0] * n
        
        for i, clause in enumerate(clauses):
            for l in clause:
                if l > 0:
                    A[i][l - 1] += 1
                else:
                    A[i][-1] -= 1
        
        return gaussian_elimination(A, b)

    def generate_random_d_regular_graphs(d, n, num_graphs):
        graphs = []
        for _ in range(num_graphs):
            graph = generate_d_regular_graph(d, n)
            if is_prime(len(graph)):
                graphs.append(graph)
        return graphs

    d = 3
    n = 10
    num_graphs = 100
    
    graphs = generate_random_d_regular_graphs(d, n, num_graphs)
    results = []
    
    for graph in graphs:
        phi = tseitin_formula(graph)
        kmi = kostant_multi_index(phi)
        w_phi = resolution_width(phi)
        results.append((kmi, w_phi))
    
    if len(results) < 100:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    kmis = [r[0] for r in results]
    widths = [r[1] for r in results]
    mean_kmi = sum(kmis) / len(kmis)
    mean_width = sum(widths) / len(widths)
    covariance = sum((k - mean_kmi) * (w - mean_width) for k, w in zip(kmis, widths))
    variance_kmi = sum((k - mean_kmi) ** 2 for k in kmis) / len(kmis)
    variance_width = sum((w - mean_width) ** 2 for w in widths) / len(widths)
    correlation = covariance / (math.sqrt(variance_kmi) * math.sqrt(variance_width))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n,
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")