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

def generate_3cnf(n, seed):
    random.seed(seed)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(int(4.5 * n)):
        clause_vars = random.sample(variables, 3)
        clause = [(v, random.choice([True, False])) for v in clause_vars]
        clauses.append(clause)
    return clauses

def is_sat(F):
    n = len(F)
    if n == 0:
        return True
    variables = set()
    for clause in F:
        for var, _ in clause:
            variables.add(var)
    variables = sorted(variables)
    for assignment in itertools.product([False, True], repeat=len(variables)):
        assignment_dict = dict(zip(variables, assignment))
        sat = True
        for clause in F:
            clause_sat = False
            for var, sign in clause:
                if assignment_dict[var] == sign:
                    clause_sat = True
                    break
            if not clause_sat:
                sat = False
                break
        if sat:
            return True
    return False

def build_conflict_graph(F):
    graph = defaultdict(set)
    for i, c1 in enumerate(F):
        for j, c2 in enumerate(F):
            if i != j:
                conflict = False
                for (v1, s1), (v2, s2) in itertools.product(c1, c2):
                    if v1 == v2 and s1 != s2:
                        conflict = True
                        break
                if conflict:
                    graph[i].add(j)
    return graph

def enumerate_independence_complex(graph, max_size=4):
    independent_sets = []
    for size in range(1, max_size + 1):
        for nodes in itertools.combinations(graph.keys(), size):
            is_independent = True
            for i, j in itertools.combinations(nodes, 2):
                if j in graph[i]:
                    is_independent = False
                    break
            if is_independent:
                independent_sets.append(set(nodes))
    return independent_sets

def greedy_lex_matching(independent_sets):
    critical_cells = []
    matched = set()
    for sigma in sorted(independent_sets, key=lambda x: (-len(x), sorted(x))):
        if sigma not in matched:
            matched.add(sigma)
            found_coface = False
            for tau in independent_sets:
                if len(tau) == len(sigma) + 1 and sigma.issubset(tau) and tau not in matched:
                    matched.add(tau)
                    found_coface = True
                    break
            if not found_coface:
                critical_cells.append(sigma)
    return critical_cells

def dpll(F):
    def backtrack(remaining, assignment):
        if not remaining:
            return 1
        leaves = 0
        for var, sign in remaining[0]:
            new_assignment = assignment.copy()
            new_assignment[var] = sign
            new_remaining = []
            for clause in remaining:
                new_clause = []
                for (v, s) in clause:
                    if v not in new_assignment or new_assignment[v] == s:
                        new_clause.append((v, s))
                if not new_clause:
                    break
                if new_clause:
                    new_remaining.append(new_clause)
            else:
                leaves += backtrack(new_remaining, new_assignment)
        return leaves
    return backtrack(F, {})

def run_trial(seed):
    n_values = [12, 16, 20, 24, 28]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        F = generate_3cnf(n, seed)
        if not is_sat(F):
            graph = build_conflict_graph(F)
            independent_sets = enumerate_independence_complex(graph)
            critical_cells = greedy_lex_matching(independent_sets)
            delta_F = len([cell for cell in critical_cells if len(cell) >= 1])
            t_star_F = dpll(F)

            if t_star_F == 0:
                continue

            log_t_star = math.log2(t_star_F)
            log_delta = math.log2(delta_F + 2)
            ratio = log_t_star / log_delta if log_delta != 0 else float('inf')

            metric_values.append(ratio)
            instances_tested += 1

            if ratio < 0.25:
                conjecture_holds = False
                counterexample = f"n={n}, log2(t*)={log_t_star}, log2(δ+2)={log_delta}, ratio={ratio}"

    if not metric_values:
        return {
            "metric_name": "log2(t*)/log2(δ+2)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2(t*)/log2(δ+2)",
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

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        if counterexamples:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")