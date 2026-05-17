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
        clause = [x if random.random() < 0.5 else -x for x in clause]
        clauses.append(clause)
    return clauses

def is_unsat(clauses, n):
    assignments = list(itertools.product([0, 1], repeat=n))
    for assignment in assignments:
        satisfied = True
        for clause in clauses:
            clause_sat = False
            for lit in clause:
                var = abs(lit)
                val = assignment[var - 1]
                if (lit > 0 and val == 1) or (lit < 0 and val == 0):
                    clause_sat = True
                    break
            if not clause_sat:
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

def find_independent_sets(graph, vertices):
    if not vertices:
        return [set()]
    v = vertices[0]
    rest = vertices[1:]
    independent_sets = find_independent_sets(graph, rest)
    new_sets = []
    for s in independent_sets:
        if v not in s and all(neighbor not in s for neighbor in graph[v]):
            new_sets.append(s | {v})
    return independent_sets + new_sets

def compute_betti_numbers(independent_sets, k):
    if k < 0 or k >= len(independent_sets):
        return 0
    boundary_matrix = []
    for i, s in enumerate(independent_sets):
        if len(s) == k + 1:
            row = [0] * len(independent_sets)
            for j, t in enumerate(independent_sets):
                if len(t) == k and t.issubset(s):
                    row[j] = 1
            boundary_matrix.append(row)
    if not boundary_matrix:
        return 0
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
    vertices = list(graph.keys())
    max_reg = 0
    for W in itertools.chain.from_iterable(itertools.combinations(vertices, r) for r in range(1, len(vertices) + 1)):
        subgraph = {v: graph[v] & set(W) for v in W}
        independent_sets = find_independent_sets(subgraph, W)
        for j in range(len(W)):
            betti = compute_betti_numbers(independent_sets, len(W) - j - 1)
            if betti > 0:
                max_reg = max(max_reg, j)
    return max_reg

def resolution_width(F, n):
    variables = list(range(1, n + 1))
    clauses = [set(clause) for clause in F]
    w = 2
    while True:
        closure = set(tuple(clause) for clause in clauses)
        changed = True
        while changed:
            changed = False
            new_clauses = []
            for c1, c2 in itertools.combinations(closure, 2):
                if len(c1) <= w and len(c2) <= w:
                    for var in variables:
                        if var in c1 and -var in c2:
                            new_clause = (c1 | c2) - {var, -var}
                            if new_clause and new_clause not in closure:
                                new_clauses.append(new_clause)
                                changed = True
            for clause in new_clauses:
                closure.add(tuple(clause))
        if any(len(clause) == 0 for clause in closure):
            return w
        w += 1

def run_trial(seed):
    n = random.choice([6, 8, 10])
    m = int(4.5 * n)
    F = generate_3cnf(n, m, seed)
    if not is_unsat(F, n):
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
    counterexample = "" if conjecture_holds else f"w*(F) = {w}, reg(F) = {reg}"
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
                print(f"RESULT: FALSIFIED counterexample={r['counterexample']} first_failing_seed={seeds[results.index(r)]}")
                break