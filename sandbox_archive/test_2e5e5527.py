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
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = []
        for var in clause_vars:
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(f'¬{var}')
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses, n):
    assignments = list(itertools.product([True, False], repeat=n))
    for assignment in assignments:
        assignment_dict = {f'x{i+1}': val for i, val in enumerate(assignment)}
        satisfied = True
        for clause in clauses:
            clause_sat = False
            for lit in clause:
                if lit.startswith('¬'):
                    var = lit[1:]
                    clause_sat = clause_sat or not assignment_dict[var]
                else:
                    clause_sat = clause_sat or assignment_dict[lit]
            satisfied = satisfied and clause_sat
            if not satisfied:
                break
        if satisfied:
            return False
    return True

def build_co_occurrence_graph(clauses, n):
    graph = {f'x{i}': set() for i in range(1, n+1)}
    for clause in clauses:
        vars_in_clause = set()
        for lit in clause:
            var = lit[1:] if lit.startswith('¬') else lit
            vars_in_clause.add(var)
        for var1, var2 in itertools.combinations(vars_in_clause, 2):
            graph[var1].add(var2)
            graph[var2].add(var1)
    return graph

def is_independent_set(graph, subset):
    for var1, var2 in itertools.combinations(subset, 2):
        if var2 in graph[var1]:
            return False
    return True

def find_independent_sets(graph, max_size):
    variables = list(graph.keys())
    independent_sets = []
    for size in range(1, max_size + 1):
        for subset in itertools.combinations(variables, size):
            if is_independent_set(graph, subset):
                independent_sets.append(set(subset))
    return independent_sets

def build_flag_complex(independent_sets):
    flag_complex = defaultdict(list)
    for size in range(1, len(independent_sets) + 1):
        for subset in itertools.combinations(independent_sets, size):
            if all(s.issubset(t) for s, t in itertools.combinations(subset, 2)):
                flag_complex[size - 1].append(set.union(*subset))
    return flag_complex

def compute_reduced_betti_numbers(flag_complex):
    betti_numbers = {}
    for k, faces in flag_complex.items():
        if not faces:
            betti_numbers[k] = 0
            continue
        # Simplified boundary matrix construction
        boundary_matrix = [[0] * len(faces) for _ in range(len(faces))]
        for i, face in enumerate(faces):
            for j, other_face in enumerate(faces):
                if face.issubset(other_face) and len(other_face) == len(face) + 1:
                    boundary_matrix[j][i] = 1
        # Gaussian elimination
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
        betti_numbers[k] = len(faces) - rank
    return betti_numbers

def compute_reg(F, n):
    graph = build_co_occurrence_graph(F, n)
    max_reg = 0
    for W_size in range(1, n + 1):
        for W in itertools.combinations(graph.keys(), W_size):
            W = set(W)
            independent_sets = find_independent_sets({k: v for k, v in graph.items() if k in W}, len(W))
            flag_complex = build_flag_complex(independent_sets)
            betti_numbers = compute_reduced_betti_numbers(flag_complex)
            for k, beta in betti_numbers.items():
                if beta > 0:
                    j = len(W) - k - 1
                    if j > max_reg:
                        max_reg = j
    return max_reg

def compute_w_star(F, n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = [set(clause) for clause in F]
    resolution_closure = set(clauses)
    w = 2
    while True:
        new_clauses = set()
        for clause1, clause2 in itertools.combinations(resolution_closure, 2):
            if len(clause1) > w or len(clause2) > w:
                continue
            common_var = None
            for lit in clause1:
                neg_lit = f'¬{lit[1:]}' if lit.startswith('¬') else f'¬{lit}'
                if neg_lit in clause2:
                    common_var = lit
                    break
            if common_var:
                resolved_clause = (clause1 - {common_var}) | (clause2 - {f'¬{common_var[1:]}' if common_var.startswith('¬') else f'¬{common_var}'})
                if len(resolved_clause) <= w:
                    new_clauses.add(frozenset(resolved_clause))
        if not new_clauses:
            break
        resolution_closure.update(new_clauses)
        if any(len(clause) == 0 for clause in resolution_closure):
            return w
        w += 1
    return float('inf')

def run_trial(seed):
    n_values = [6, 8, 10]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        alpha = 4.5
        F = generate_random_3cnf(n, alpha, seed)
        if not is_unsatisfiable(F, n):
            continue
        reg_F = compute_reg(F, n)
        w_star_F = compute_w_star(F, n)
        if w_star_F < reg_F + 2:
            conjecture_holds = False
            counterexample = f"F with n={n}, reg(F)={reg_F}, w*(F)={w_star_F}"
            break
        metric_values.append(w_star_F - reg_F)
        instances_tested += 1
    if not metric_values:
        return {
            "metric_name": "w*(F) - reg(F)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No unsatisfiable instances generated"
        }
    return {
        "metric_name": "w*(F) - reg(F)",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
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
    metric_values = [r["metric_value"] for r in results if r["metric_value"] != 0.0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")