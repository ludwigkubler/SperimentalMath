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
    
    def generate_tseitin_formula(n, d):
        if n % d != 0:
            return None
        vertices = list(range(n))
        edges = set()
        for i in range(n):
            neighbors = random.sample(vertices[:i] + vertices[i+1:], d-1)
            for neighbor in neighbors:
                edge = tuple(sorted((i, neighbor)))
                if edge not in edges and (neighbor, i) not in edges:
                    edges.add(edge)
        return vertices, edges
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            pivot_row = -1
            for i in range(rank, m):
                if A[i][j] != 0:
                    pivot_row = i
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    factor = A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def resolution_length(formula):
        vertices, edges = formula
        n = len(vertices)
        m = len(edges)
        clauses = []
        for u, v in edges:
            clauses.append([u, -v])
            clauses.append([-u, v])
        clauses.append([-1] * n + [1])
        queue = clauses[:]
        seen = set()
        while queue:
            clause = queue.pop(0)
            if all(x not in seen for x in clause):
                seen.update(clause)
                for other_clause in clauses:
                    new_clause = []
                    for x in other_clause:
                        if -x in clause:
                            continue
                        if x in clause:
                            break
                        else:
                            new_clause.append(x)
                    if len(new_clause) == 0:
                        return len(clauses)
                    elif len(new_clause) > 1:
                        queue.append(new_clause)
        return len(clauses)
    
    def minimal_order_of_modular_forms(formula):
        vertices, edges = formula
        n = len(vertices)
        m = len(edges)
        A = [[0] * (n + m) for _ in range(n)]
        for i, u in enumerate(vertices):
            A[i][i] = 1
        for j, (u, v) in enumerate(edges):
            A[u][n + j] = 1
            A[v][n + j] = -1
        rank = gaussian_elimination(A)
        return n - rank
    
    def tseitin_formula_to_lattice(formula):
        vertices, edges = formula
        n = len(vertices)
        m = len(edges)
        lattice = [[0] * (n + m) for _ in range(n)]
        for i, u in enumerate(vertices):
            lattice[i][i] = 1
        for j, (u, v) in enumerate(edges):
            lattice[u][n + j] = 1
            lattice[v][n + j] = -1
        return lattice
    
    def hecke_operator(lattice, k):
        n = len(lattice)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    result[i][j] = 1
                else:
                    result[i][j] = lattice[i][j]
        return result
    
    def minimal_order_of_modular_forms_hecke(formula, k):
        vertices, edges = formula
        n = len(vertices)
        m = len(edges)
        lattice = tseitin_formula_to_lattice(formula)
        for _ in range(k):
            lattice = hecke_operator(lattice, k)
        rank = gaussian_elimination(lattice)
        return n - rank
    
    def generate_random_d_regular_graph(n, d):
        if n % d != 0:
            return None
        vertices = list(range(n))
        edges = set()
        for i in range(n):
            neighbors = random.sample(vertices[:i] + vertices[i+1:], d-1)
            for neighbor in neighbors:
                edge = tuple(sorted((i, neighbor)))
                if edge not in edges and (neighbor, i) not in edges:
                    edges.add(edge)
        return vertices, edges
    
    def resolution_length_d_regular_graph(n, d):
        formula = generate_random_d_regular_graph(n, d)
        if formula is None:
            return None
        return resolution_length(formula)
    
    def minimal_order_of_modular_forms_d_regular_graph(n, d):
        formula = generate_random_d_regular_graph(n, d)
        if formula is None:
            return None
        return minimal_order_of_modular_forms(formula)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        resolution_lengths = []
        modular_orders = []
        for _ in range(5):
            length = resolution_length_d_regular_graph(n, n)
            if length is None:
                continue
            order = minimal_order_of_modular_forms_d_regular_graph(n, n)
            if order is None:
                continue
            resolution_lengths.append(length)
            modular_orders.append(order)
        if len(resolution_lengths) < 3 or len(modular_orders) < 3:
            continue
        correlation_coefficient = sum((resolution_lengths[i] - mean(resolution_lengths)) * (modular_orders[i] - mean(modular_orders)) for i in range(len(resolution_lengths))) / math.sqrt(sum((resolution_lengths[i] - mean(resolution_lengths))**2 for i in range(len(resolution_lengths)))) / math.sqrt(sum((modular_orders[i] - mean(modular_orders))**2 for i in range(len(modular_orders))))
        p_value = 2 * (1 - scipy.stats.norm.cdf(abs(correlation_coefficient) * math.sqrt(len(resolution_lengths) - 2)))
        results.append({"n": n, "correlation_coefficient": correlation_coefficient, "p_value": p_value})
    
    if not results:
        return {"metric_name": "Correlation Coefficient", "metric_value": None, "instances_tested": 0, "n_max": 0, "conjecture_holds": False, "counterexample": "No valid instances found"}
    
    mean_correlation_coefficient = mean([result["correlation_coefficient"] for result in results])
    p_values = [result["p_value"] for result in results]
    max_p_value = max(p_values)
    
    return {"metric_name": "Correlation Coefficient", "metric_value": mean_correlation_coefficient, "instances_tested": len(results), "n_max": max([result["n"] for result in results]), "conjecture_holds": mean_correlation_coefficient >= 0.7 and max_p_value <= 0.05, "counterexample": "" if mean_correlation_coefficient >= 0.7 and max_p_value <= 0.05 else "Correlation coefficient < 0.7 or p-value > 0.05"}

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "Correlation coefficient < 0.7 or p-value > 0.05"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")