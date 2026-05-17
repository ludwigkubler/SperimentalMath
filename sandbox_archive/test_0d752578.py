# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_3cnf(n, m, seed):
    random.seed(seed)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        clause = [(var, random.choice([True, False])) for var in clause]
        clauses.append(clause)
    return clauses

def is_unsatisfiable(F, n):
    assignments = itertools.product([False, True], repeat=n)
    for assignment in assignments:
        satisfied = True
        for clause in F:
            clause_satisfied = False
            for var, sign in clause:
                if assignment[var - 1] == sign:
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                satisfied = False
                break
        if satisfied:
            return False
    return True

def build_co_occurrence_graph(F, n):
    graph = defaultdict(set)
    for clause in F:
        variables = [var for var, _ in clause]
        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                graph[variables[i]].add(variables[j])
                graph[variables[j]].add(variables[i])
    return graph

def find_independent_sets(graph, W):
    if not W:
        return [frozenset()]
    v = W[0]
    independent_sets = []
    for subset in find_independent_sets(graph, W[1:]):
        independent_sets.append(subset)
        if all(u not in subset for u in graph[v]):
            independent_sets.append(subset | {v})
    return independent_sets

def compute_betti_numbers(independent_sets, k):
    if k < 0 or k >= len(independent_sets):
        return 0
    boundary_matrix = [[0] * len(independent_sets) for _ in range(len(independent_sets))]
    for i, sigma in enumerate(independent_sets):
        for j, tau in enumerate(independent_sets):
            if sigma.issuperset(tau) and len(sigma) == len(tau) + 1:
                boundary_matrix[i][j] = 1
    rank = 0
    for col in range(len(boundary_matrix[0])):
        pivot = -1
        for row in range(rank, len(boundary_matrix)):
            if boundary_matrix[row][col] == 1:
                pivot = row
                break
        if pivot == -1:
            continue
        boundary_matrix[rank], boundary_matrix[pivot] = boundary_matrix[pivot], boundary_matrix[rank]
        for row in range(len(boundary_matrix)):
            if row != rank and boundary_matrix[row][col] == 1:
                for c in range(len(boundary_matrix[0])):
                    boundary_matrix[row][c] ^= boundary_matrix[rank][c]
        rank += 1
    return len(boundary_matrix) - rank

def compute_reg(F, n):
    graph = build_co_occurrence_graph(F, n)
    max_reg = 0
    for W in itertools.chain.from_iterable(itertools.combinations(range(1, n + 1), r) for r in range(1, n + 1)):
        independent_sets = find_independent_sets(graph, list(W))
        for j in range(len(W) + 1):
            if compute_betti_numbers(independent_sets, len(W) - j - 1) > 0:
                max_reg = max(max_reg, j)
    return max_reg

def resolution_width(F, n):
    clauses = [frozenset((var, sign) for var, sign in clause) for clause in F]
    closure = set(clauses)
    w = 2
    while True:
        new_clauses = set()
        for c1, c2 in itertools.combinations(closure, 2):
            common_vars = set(var for var, _ in c1) & set(var for var, _ in c2)
            for var in common_vars:
                if any((var, True) in c1 and (var, False) in c2) or any((var, False) in c1 and (var, True) in c2):
                    new_clause = (c1 | c2) - {(var, True), (var, False)}
                    if len(new_clause) <= w:
                        new_clauses.add(new_clause)
        if not new_clauses:
            break
        closure.update(new_clauses)
        if any(len(clause) == 0 for clause in closure):
            return w
        w += 1
    return float('inf')

def run_trial(seed):
    n = random.choice([6, 8, 10])
    m = int(4.5 * n)
    F = generate_3cnf(n, m, seed)
    if not is_unsatisfiable(F, n):
        return {
            "metric_name": "w*(F) - reg(F)",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    reg = compute_reg(F, n)
    w = resolution_width(F, n)
    metric_value = w - reg
    conjecture_holds = metric_value >= 2
    counterexample = "" if conjecture_holds else f"w*(F) = {w} < reg(F) + 2 = {reg + 2}"
    return {
        "metric_name": "w*(F) - reg(F)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seeds[results.index(r)]}")
                break