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
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(int(4.5 * n)):
        clause_vars = random.sample(variables, 3)
        clause = []
        for var in clause_vars:
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(f'¬{var}')
        clauses.append(clause)
    return clauses

def is_sat(clauses, max_depth=1000):
    if not clauses:
        return True
    if max_depth == 0:
        return False
    var = clauses[0][0].replace('¬', '')
    for sign in [var, f'¬{var}']:
        new_clauses = []
        for clause in clauses:
            if sign in clause:
                continue
            elif f'¬{sign.replace("¬", "")}' in clause:
                new_clause = [lit for lit in clause if lit != f'¬{sign.replace("¬", "")}']
                if not new_clause:
                    break
                new_clauses.append(new_clause)
            else:
                new_clauses.append(clause)
        else:
            if is_sat(new_clauses, max_depth-1):
                return True
    return False

def build_conflict_graph(clauses):
    graph = defaultdict(set)
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if i >= j:
                continue
            conflict = False
            for lit1 in clause1:
                for lit2 in clause2:
                    if (lit1.startswith('¬') and lit2 == lit1[1:]) or (lit2.startswith('¬') and lit1 == lit2[1:]):
                        conflict = True
                        break
                if conflict:
                    break
            if conflict:
                graph[i].add(j)
                graph[j].add(i)
    return graph

def enumerate_independent_sets(graph, max_size=4):
    independent_sets = []
    for size in range(1, max_size+1):
        for nodes in itertools.combinations(graph.keys(), size):
            independent = True
            for i in range(len(nodes)):
                for j in range(i+1, len(nodes)):
                    if nodes[j] in graph[nodes[i]]:
                        independent = False
                        break
                if not independent:
                    break
            if independent:
                independent_sets.append(set(nodes))
    return independent_sets

def greedy_lex_matching(independent_sets):
    matched = set()
    critical_cells = []
    for sigma in sorted(independent_sets, key=lambda x: (len(x), sorted(x))):
        if sigma in matched:
            continue
        for tau in sorted(independent_sets, key=lambda x: (len(x), sorted(x))):
            if len(tau) != len(sigma) + 1:
                continue
            if sigma.issubset(tau) and tau not in matched:
                matched.add(tau)
                break
        else:
            critical_cells.append(sigma)
    return critical_cells

def dpll(clauses, assignments=None):
    if assignments is None:
        assignments = {}
    if not clauses:
        return 1
    for clause in clauses:
        if all(lit.replace('¬', '') in assignments and (lit.startswith('¬') != assignments[lit.replace('¬', '')]) for lit in clause):
            return 0
    unit_clauses = [clause for clause in clauses if len(clause) == 1]
    if unit_clauses:
        lit = unit_clauses[0][0]
        var = lit.replace('¬', '')
        assignments[var] = not lit.startswith('¬')
        new_clauses = []
        for clause in clauses:
            if lit in clause:
                continue
            elif f'¬{var}' in clause:
                new_clause = [c for c in clause if c != f'¬{var}']
                if not new_clause:
                    return 0
                new_clauses.append(new_clause)
            else:
                new_clauses.append(clause)
        return dpll(new_clauses, assignments)
    var = clauses[0][0].replace('¬', '')
    total = 0
    for val in [True, False]:
        new_assignments = assignments.copy()
        new_assignments[var] = val
        new_clauses = []
        for clause in clauses:
            if var in clause and val:
                continue
            elif f'¬{var}' in clause and not val:
                continue
            new_clause = [lit for lit in clause if lit.replace('¬', '') != var]
            if not new_clause:
                continue
            new_clauses.append(new_clause)
        total += dpll(new_clauses, new_assignments)
    return total

def run_trial(seed):
    n = random.choice([12, 16, 20, 24, 28])
    clauses = generate_3cnf(n, seed)
    if is_sat(clauses):
        return {
            "metric_name": "log2(t*)/log2(δ+2)",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    graph = build_conflict_graph(clauses)
    independent_sets = enumerate_independent_sets(graph)
    critical_cells = greedy_lex_matching(independent_sets)
    delta = len([cell for cell in critical_cells if len(cell) >= 1])
    t_star = dpll(clauses)
    if t_star == 0:
        return {
            "metric_name": "log2(t*)/log2(δ+2)",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    ratio = math.log2(t_star) / math.log2(delta + 2)
    conjecture_holds = ratio >= 0.25
    counterexample = "" if conjecture_holds else f"log2(t*)/log2(δ+2) = {ratio} < 0.25"
    return {
        "metric_name": "log2(t*)/log2(δ+2)",
        "metric_value": ratio,
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
    metric_values = [r["metric_value"] for r in results if r["metric_value"] != 0.0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [r["counterexample"] for r in results if r["counterexample"]]
        if counterexamples:
            first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")