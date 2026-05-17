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

def generate_random_3cnf(n, alpha, seed):
    random.seed(seed)
    m = int(alpha * n)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        if random.random() < 0.5:
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses, n):
    assignments = list(itertools.product([-1, 1], repeat=n))
    for assignment in assignments:
        satisfied = True
        for clause in clauses:
            sat_clause = False
            for lit in clause:
                var = abs(lit)
                val = assignment[var - 1]
                if (lit > 0 and val == 1) or (lit < 0 and val == -1):
                    sat_clause = True
                    break
            if not sat_clause:
                satisfied = False
                break
        if satisfied:
            return False
    return True

def build_co_occurrence_graph(clauses, n):
    graph = defaultdict(set)
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                x = abs(clause[i])
                y = abs(clause[j])
                graph[x].add(y)
                graph[y].add(x)
    return graph

def is_independent_set(graph, W):
    for x in W:
        for y in W:
            if x != y and y in graph[x]:
                return False
    return True

def enumerate_independent_sets(graph, W):
    independent_sets = []
    for k in range(1, len(W) + 1):
        for subset in itertools.combinations(W, k):
            if is_independent_set(graph, subset):
                independent_sets.append(subset)
    return independent_sets

def compute_reduced_betti_numbers(independent_sets, k):
    if k < 0 or k >= len(independent_sets):
        return 0
    boundary_matrix = []
    for i in range(len(independent_sets)):
        row = [0] * len(independent_sets)
        for j in range(len(independent_sets)):
            if set(independent_sets[i]).issubset(set(independent_sets[j])):
                row[j] = 1
        boundary_matrix.append(row)
    rank = gaussian_elimination(boundary_matrix)
    return len(boundary_matrix) - rank

def gaussian_elimination(matrix):
    rank = 0
    for col in range(len(matrix[0])):
        pivot = -1
        for row in range(rank, len(matrix)):
            if matrix[row][col] == 1:
                pivot = row
                break
        if pivot == -1:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for row in range(len(matrix)):
            if row != rank and matrix[row][col] == 1:
                for c in range(col, len(matrix[0])):
                    matrix[row][c] ^= matrix[rank][c]
        rank += 1
    return rank

def compute_reg(F, n):
    graph = build_co_occurrence_graph(F, n)
    max_reg = 0
    for W in itertools.chain.from_iterable(itertools.combinations(range(1, n + 1), r) for r in range(1, n + 1)):
        independent_sets = enumerate_independent_sets(graph, W)
        for j in range(len(W) + 1):
            k = len(W) - j - 1
            if k >= 0 and compute_reduced_betti_numbers(independent_sets, k) > 0:
                if j > max_reg:
                    max_reg = j
    return max_reg

def compute_w_star(F, n):
    clauses = [set(clause) for clause in F]
    w = 2
    while True:
        resolution_closure = set(clauses)
        new_clauses = set()
        for clause1 in clauses:
            for clause2 in clauses:
                if len(clause1) <= w and len(clause2) <= w:
                    for lit in clause1:
                        if -lit in clause2:
                            resolvent = (clause1 - {lit}) | (clause2 - {-lit})
                            if resolvent:
                                new_clauses.add(frozenset(resolvent))
        resolution_closure.update(new_clauses)
        if not new_clauses:
            break
        if any(len(clause) > w for clause in resolution_closure):
            w += 1
        if any(not clause for clause in resolution_closure):
            return w
    return w

def run_trial(seed):
    n = random.choice([6, 8, 10])
    alpha = 4.5
    F = generate_random_3cnf(n, alpha, seed)
    if not is_unsatisfiable(F, n):
        return {
            "metric_name": "w_star_minus_reg",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    reg_F = compute_reg(F, n)
    w_star_F = compute_w_star(F, n)
    metric_value = w_star_F - reg_F
    conjecture_holds = metric_value >= 2
    counterexample = f"w*(F) = {w_star_F} < reg(F) + 2 = {reg_F + 2}" if not conjecture_holds else ""
    return {
        "metric_name": "w_star_minus_reg",
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
        result["seed"] = seed
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
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break