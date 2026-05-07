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
    
    def generate_graph(n, density):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < density:
                    edges.add((i, j))
        return list(edges)
    
    def is_connected(graph, n):
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph:
                    if neighbor[0] == node and not visited[neighbor[1]]:
                        stack.append(neighbor[1])
                    elif neighbor[1] == node and not visited[neighbor[0]]:
                        stack.append(neighbor[0])
        return all(visited)
    
    def add_odd_parity_charge(graph, n):
        charge = [random.choice([0, 1]) for _ in range(n)]
        for i in range(n):
            parity = sum(charge[j] for j, (_, j) in enumerate(graph) if j != i) % 2
            charge[i] += parity
        return charge
    
    def tseitin_cnf(graph, n, charge):
        cnf = []
        literals = {i: [0, 1] for i in range(n)}
        for i in range(n):
            clause = [literals[i][charge[i]]]
            for j, (_, j) in enumerate(graph):
                if j == i:
                    continue
                clause.append(literals[j][1 - charge[j]])
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, literals):
        def propagate():
            while True:
                changed = False
                for clause in cnf:
                    if len(clause) == 0:
                        return None
                    unit_clauses = [l for l in clause if literals[l] == -1]
                    if unit_clauses:
                        literal = unit_clauses[0]
                        literals[literal] = 1 - (literal % 2)
                        changed = True
                if not changed:
                    break
        
        def backtrack(level):
            while level < len(cnf) and literals[cnf[level][0]] != -1:
                level += 1
            if level == len(cnf):
                return True
            literal = cnf[level][0]
            literals[literal] = 1 - (literal % 2)
            if backtrack(level + 1):
                return True
            literals[literal] = -1
            literals[1 - literal] = -1
            return backtrack(level + 1)
        
        propagate()
        if None in cnf:
            return None
        if backtrack(0):
            return literals
    
    def smith_normal_form(matrix):
        n = len(matrix)
        for i in range(n):
            pivot_row = i
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    return [0] * n
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] // matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return [matrix[i][i] for i in range(n)]
    
    def laplacian_matrix(graph, n):
        laplacian = [[0] * n for _ in range(n)]
        degree = [sum(1 for _, j in graph if j == i) for i in range(n)]
        for i, (_, j) in enumerate(graph):
            laplacian[i][j] = -1
            laplacian[j][i] = -1
        for i in range(n):
            laplacian[i][i] = degree[i]
        return laplacian
    
    def reduced_laplacian(laplacian, n):
        return [row[1:] for row in laplacian[1:]]
    
    def tree_resolution_size(cnf):
        literals = {i: -1 for i in range(2 * len(cnf))}
        stack = []
        while cnf:
            clause = cnf.pop()
            if len(clause) == 0:
                return None
            unit_clauses = [l for l in clause if literals[l] == -1]
            if unit_clauses:
                literal = unit_clauses[0]
                literals[literal] = 1 - (literal % 2)
                stack.append(literal)
            else:
                literal = min(clause, key=lambda x: literals[x])
                literals[literal] = 1 - (literal % 2)
                for j in range(len(cnf)):
                    if literal in cnf[j]:
                        cnf[j].remove(literal)
        return len(stack)
    
    n_values = [6, 8, 10, 12, 14, 16, 18, 20]
    densities = [3 + i for i in range(3)]
    results = []
    
    for n in n_values:
        for density in densities:
            graph = generate_graph(n, density)
            if not is_connected(graph, n):
                continue
            charge = add_odd_parity_charge(graph, n)
            cnf = tseitin_cnf(graph, n, charge)
            literals = dpll(cnf, {})
            size_TR = tree_resolution_size(cnf) if literals else None
            if size_TR is not None:
                laplacian = laplacian_matrix(graph, n)
                reduced_lap = reduced_laplacian(laplacian, n)
                snf = smith_normal_form(reduced_lap)
                r_2 = sum(1 for s in snf if s % 2 == 0)
                results.append({
                    "n": n,
                    "density": density,
                    "size_TR": size_TR,
                    "r_2": r_2
                })
    
    mean_size_TR = sum(result["size_TR"] for result in results) / len(results)
    std_size_TR = math.sqrt(sum((result["size_TR"] - mean_size_TR) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["size_TR"] >= result["n"] * (2 ** result["r_2"])) / len(results)
    
    return {
        "metric_name": "tree_resolution_size",
        "metric_value": mean_size_TR,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1.0,
        "counterexample": "" if support_fraction == 1.0 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_size_TR = sum(result["metric_value"] for result in results) / len(results)
    std_size_TR = math.sqrt(sum((result["metric_value"] - mean_size_TR) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_size_TR} std={std_size_TR} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")