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
        if (n * d) % 2 != 0 or d < 1 or n < 1:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        literals = {}
        for i in range(n):
            literals[i] = random.randint(1, 2 * n)
        for i in range(n):
            clause = [-literals[i]]
            for j in graph[i]:
                clause.append(literals[j])
            clauses.append(clause)
            for j in graph[i]:
                for k in graph[j]:
                    if k != i:
                        clauses.append([-literals[i], -literals[j], literals[k]])
        return clauses
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            pivot_row = None
            for i in range(rank, m):
                if matrix[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for i in range(m):
                    if i != rank and matrix[i][j] != 0:
                        factor = -matrix[i][j] / matrix[rank][j]
                        for k in range(n):
                            matrix[i][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    def minimal_index(graph):
        n = len(graph)
        clauses = tseitin_formula(graph)
        m = len(clauses)
        matrix = [[0] * (n + m) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if j in graph[i // 2]:
                    matrix[i][j] = -1
                else:
                    matrix[i][j] = 1
            matrix[i][n + i] = 1
        return gaussian_elimination(matrix)
    
    def resolution_width(clauses):
        n = len(clauses)
        queue = clauses[:]
        resolvents = set()
        while queue:
            clause = queue.pop(0)
            if not any(lit in resolvents for lit in clause):
                resolvents.add(tuple(sorted(clause)))
                for i in range(n):
                    if any(-lit in clause and -other_lit in clauses[i] for lit, other_lit in zip(clause, clauses[i])):
                        new_clause = sorted(list(set(clause) ^ set(clauses[i])))
                        if new_clause not in queue:
                            queue.append(new_clause)
        return len(resolvents)
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if graph is None:
        return {
            "metric_name": "m_index(G)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_index = minimal_index(graph)
    phi = tseitin_formula(graph)
    w_phi = resolution_width(phi)
    
    return {
        "metric_name": "m_index(G)",
        "metric_value": m_index,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": m_index <= 10 and abs(m_index - w_phi) < 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        mean_m_index = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_m_index) ** 2 for r in results) / len(results))
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_m_index:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            counterexample = "m_index(G) > 10 or |m_index(G) - w(φ_G)| >= 3"
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")