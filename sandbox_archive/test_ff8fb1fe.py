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
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for neighbor in graph[i]:
                clause.append(f"~{literals[neighbor]}")
            clauses.append(clause)
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if (i, j) not in graph and (j, i) not in graph:
                        clauses.append([f"{literals[i]}", f"{literals[j]}"])
                        clauses.append([f"~{literals[i]}", f"~{literals[j]}"])
                        clauses.append([f"{literals[j]}", f"{literals[k]}"])
                        clauses.append([f"~{literals[j]}", f"~{literals[k]}"])
        return literals, clauses
    
    def resolution_width(clauses):
        queue = [clause for clause in clauses if len(clause) == 1]
        learned_clauses = []
        while queue:
            unit_clause = next((c for c in queue if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            queue.remove(unit_clause)
            for clause in clauses:
                if literal in clause:
                    learned_clauses.append([l for l in clause if l != literal])
                elif f"~{literal}" in clause:
                    learned_clauses.append([l for l in clause if l != f"~{literal}"])
        return len(learned_clauses)
    
    def alexander_orlik_solomon_complexity(graph):
        n = len(graph)
        generators = []
        for i in range(n):
            generator = [0] * n
            generator[i] = 1
            generators.append(generator)
        return len(generators)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                    i_max = i
            if matrix[i_max][j] == 0:
                continue
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for i in range(m):
                if i != rank and matrix[i][j] != 0:
                    factor = Fraction(matrix[i][j], matrix[rank][j])
                    for k in range(n):
                        matrix[i][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def alexander_module_rank(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                adjacency_matrix[i][j] = 1
        return gaussian_elimination(adjacency_matrix)
    
    def min_alexander_orlik_solomon_complexity(graph):
        return alexander_module_rank(graph)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_d_regular_graph(n, d=2)  # Example: generating a 2-regular graph
        if not graph:
            continue
        literals, clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        complexity = min_alexander_orlik_solomon_complexity(graph)
        results.append({
            "n": n,
            "width": width,
            "complexity": complexity
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_width = sum(result["width"] for result in results) / len(results)
    mean_complexity = sum(result["complexity"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["width"] - result["complexity"]) <= 10) / len(results)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"width={mean_width}, complexity={mean_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=NA support_fraction={support_fraction}")
    elif any(result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=support_fraction_too_low support_fraction={support_fraction}")