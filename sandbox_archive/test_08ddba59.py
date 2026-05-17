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

def generate_3cnf(seed, n):
    random.seed(seed)
    m = int(4.5 * n)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = []
        for var in clause_vars:
            if random.random() < 0.5:
                clause.append(-var)
            else:
                clause.append(var)
        clauses.append(clause)
    return clauses

def is_sat(clauses):
    n = max(abs(var) for clause in clauses for var in clause)
    assignments = list(itertools.product([False, True], repeat=n))
    for assignment in assignments:
        sat = True
        for clause in clauses:
            clause_sat = False
            for lit in clause:
                var = abs(lit) - 1
                val = assignment[var]
                if lit < 0:
                    val = not val
                if val:
                    clause_sat = True
                    break
            if not clause_sat:
                sat = False
                break
        if sat:
            return True
    return False

def build_conflict_graph(clauses):
    graph = defaultdict(set)
    for i, c1 in enumerate(clauses):
        for j, c2 in enumerate(clauses):
            if i != j:
                conflict = False
                for lit1 in c1:
                    for lit2 in c2:
                        if lit1 == -lit2:
                            conflict = True
                            break
                    if conflict:
                        break
                if conflict:
                    graph[i].add(j)
    return graph

def enumerate_independence_complex(graph, max_size=4):
    n = len(graph)
    independent_sets = []
    for size in range(1, max_size + 1):
        for vertices in itertools.combinations(range(n), size):
            independent = True
            for i, v1 in enumerate(vertices):
                for v2 in vertices[i+1:]:
                    if v2 in graph[v1]:
                        independent = False
                        break
                if not independent:
                    break
            if independent:
                independent_sets.append(vertices)
    return independent_sets

def greedy_lex_matching(independent_sets):
    independent_sets.sort(key=lambda x: (len(x), x))
    matched = set()
    critical_cells = []
    for sigma in independent_sets:
        if sigma not in matched:
            matched.add(sigma)
            found_coface = False
            for tau in independent_sets:
                if tau not in matched and set(sigma).issubset(tau) and len(tau) == len(sigma) + 1:
                    matched.add(tau)
                    found_coface = True
                    break
            if not found_coface:
                critical_cells.append(sigma)
    return critical_cells

def dpll(clauses, assignment=None, depth=0):
    if assignment is None:
        n = max(abs(var) for clause in clauses for var in clause)
        assignment = [None] * n
    if depth == len(assignment):
        return True
    var = depth + 1
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var - 1] = val
        if all(any((lit < 0 and not new_assignment[abs(lit) - 1]) or (lit > 0 and new_assignment[abs(lit) - 1]) for lit in clause) for clause in clauses):
            if dpll(clauses, new_assignment, depth + 1):
                return True
    return False

def count_dpll_leaves(clauses, assignment=None, depth=0):
    if assignment is None:
        n = max(abs(var) for clause in clauses for var in clause)
        assignment = [None] * n
    if depth == len(assignment):
        return 1
    var = depth + 1
    leaves = 0
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var - 1] = val
        if all(any((lit < 0 and not new_assignment[abs(lit) - 1]) or (lit > 0 and new_assignment[abs(lit) - 1]) for lit in clause) for clause in clauses):
            leaves += count_dpll_leaves(clauses, new_assignment, depth + 1)
    return leaves

def run_trial(seed):
    n_values = [12, 16, 20, 24, 28]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        clauses = generate_3cnf(seed, n)
        if not is_sat(clauses):
            graph = build_conflict_graph(clauses)
            independent_sets = enumerate_independence_complex(graph)
            critical_cells = greedy_lex_matching(independent_sets)
            delta = len([cell for cell in critical_cells if len(cell) >= 1])
            t_star = count_dpll_leaves(clauses)
            if t_star <= 0 or delta + 2 <= 0:
                continue
            log_t_star = math.log2(t_star)
            log_delta = math.log2(delta + 2)
            if log_t_star < 0.25 * log_delta:
                conjecture_holds = False
                counterexample = f"n={n}, log_t_star={log_t_star}, log_delta={log_delta}"
                break
            metric_values.append(log_t_star / log_delta)
            instances_tested += 1

    if not metric_values:
        return {
            "metric_name": "log2(t*(F))/log2(δ(F)+2)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2(t*(F))/log2(δ(F)+2)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
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

    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        if first_failing_seed is not None:
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")