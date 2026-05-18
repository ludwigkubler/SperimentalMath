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

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    for i in range(n):
        j = (i + 2) % n
        edges.append((vertices[i], vertices[j]))
    return edges

def generate_tseitin_formula(n):
    edges = generate_3_regular_graph(n)
    clauses = []
    for u, v in edges:
        x = random.randint(0, 1)
        y = random.randint(0, 1)
        z = random.randint(0, 1)
        clauses.append([(u, x), (v, y), (n + u, z)])
        clauses.append([(u, 1 - x), (v, 1 - y), (n + u, 1 - z)])
    return clauses

def generate_random_3_sat(n, m):
    clauses = []
    for _ in range(m):
        clause = []
        for _ in range(3):
            lit = random.randint(0, 2 * n - 1)
            clause.append((lit // 2, lit % 2))
        clauses.append(clause)
    return clauses

def generate_2_xor_sat_lifted(n, m):
    clauses = []
    for _ in range(m):
        a = random.randint(0, n - 1)
        b = random.randint(0, n - 1)
        c = random.randint(0, n - 1)
        clauses.append([(a, 0), (b, 0), (c, 1)])
        clauses.append([(a, 1), (b, 1), (c, 1)])
    return clauses

def is_unsatisfiable(formula):
    n = max(max(abs(lit) for lit in clause) for clause in formula) + 1
    assignments = itertools.product([0, 1], repeat=n)
    for assignment in assignments:
        satisfied = True
        for clause in formula:
            clause_sat = False
            for lit in clause:
                var, val = lit
                if assignment[var] == val:
                    clause_sat = True
                    break
            if not clause_sat:
                satisfied = False
                break
        if satisfied:
            return False
    return True

def build_variable_sharing_graph(formula):
    n = max(max(abs(lit) for lit in clause) for clause in formula) + 1
    graph = defaultdict(set)
    for i, clause1 in enumerate(formula):
        for j, clause2 in enumerate(formula):
            if i != j:
                shared_vars = set()
                for lit1 in clause1:
                    for lit2 in clause2:
                        if lit1[0] == lit2[0]:
                            shared_vars.add(lit1[0])
                if len(shared_vars) >= 1:
                    graph[i].add(j)
    return graph

def enumerate_cliques(graph, max_size):
    cliques = []
    vertices = list(graph.keys())
    for size in range(2, max_size + 1):
        for candidate in itertools.combinations(vertices, size):
            is_clique = True
            for i in range(size):
                for j in range(i + 1, size):
                    if candidate[j] not in graph[candidate[i]]:
                        is_clique = False
                        break
                if not is_clique:
                    break
            if is_clique:
                cliques.append(candidate)
    return cliques

def compute_cartier_foata_polynomial(cliques, q):
    result = 0.0
    for clique in cliques:
        result += (-q) ** len(clique)
    return result

def find_positive_root(cliques, max_q):
    for q in [0.1 * i for i in range(1, int(max_q * 10) + 1)]:
        if compute_cartier_foata_polynomial(cliques, q) == 0:
            return q
    return float('inf')

def compute_max_degree(graph):
    return max(len(neighbors) for neighbors in graph.values()) if graph else 0

def run_dpll(formula):
    n = max(max(abs(lit) for lit in clause) for clause in formula) + 1
    assignments = [None] * n
    return dpll_recursive(formula, assignments)

def dpll_recursive(formula, assignments):
    if not formula:
        return True
    if any(not clause for clause in formula):
        return False
    for clause in formula:
        if len(clause) == 1:
            lit = clause[0]
            var, val = lit
            if assignments[var] is not None and assignments[var] != val:
                return False
            assignments[var] = val
            new_formula = [c for c in formula if lit not in c]
            return dpll_recursive(new_formula, assignments)
    for clause in formula:
        if len(clause) == 2:
            lit1, lit2 = clause
            var1, val1 = lit1
            var2, val2 = lit2
            if assignments[var1] is None and assignments[var2] is None:
                assignments[var1] = val1
                assignments[var2] = val2
                new_formula = [c for c in formula if lit1 not in c and lit2 not in c]
                if dpll_recursive(new_formula, assignments):
                    return True
                assignments[var1] = 1 - val1
                assignments[var2] = 1 - val2
                new_formula = [c for c in formula if lit1 not in c and lit2 not in c]
                if dpll_recursive(new_formula, assignments):
                    return True
                assignments[var1] = None
                assignments[var2] = None
                return False
    lit = random.choice([lit for clause in formula for lit in clause])
    var, val = lit
    assignments[var] = val
    new_formula = [c for c in formula if lit not in c]
    if dpll_recursive(new_formula, assignments):
        return True
    assignments[var] = 1 - val
    new_formula = [c for c in formula if lit not in c]
    return dpll_recursive(new_formula, assignments)

def run_trial(seed):
    random.seed(seed)
    n_values = [12, 16, 20, 24, 28, 32, 36, 40]
    ensemble_types = ['tseitin', 'random_3_sat', '2_xor_sat_lifted']
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        for ensemble_type in ensemble_types:
            if ensemble_type == 'tseitin':
                formula = generate_tseitin_formula(n)
            elif ensemble_type == 'random_3_sat':
                m = int(4.4 * n)
                formula = generate_random_3_sat(n, m)
            elif ensemble_type == '2_xor_sat_lifted':
                m = int(4.4 * n)
                formula = generate_2_xor_sat_lifted(n, m)

            if not is_unsatisfiable(formula):
                continue

            graph = build_variable_sharing_graph(formula)
            cliques = enumerate_cliques(graph, 6)
            r = find_positive_root(cliques, 1.0)
            delta = compute_max_degree(graph)
            t_star = run_dpll(formula)
            log_t_star = math.log2(t_star) if t_star > 0 else 0
            metric_value = log_t_star / (1 / r - delta) if (1 / r - delta) != 0 else 0
            metric_values.append(metric_value)

            if metric_value < 0.5 * (1 / r - delta) - 1:
                conjecture_holds = False
                counterexample = f"n={n}, ensemble={ensemble_type}, log_t_star={log_t_star}, r={r}, delta={delta}"
                break

            instances_tested += 1

            if not conjecture_holds:
                break

        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "log_t_star / (1/r - delta)",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = (sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) ** 0.5

    return {
        "metric_name": "log_t_star / (1/r - delta)",
        "metric_value": mean_metric,
        "std_metric": std_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trials.append(trial)
        print(f"TRIAL: {trial}")

    metric_values = [trial["metric_value"] for trial in trials if "metric_value" in trial]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_metric_values")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = (sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexamples = [trial["counterexample"] for trial in trials if not trial["conjecture_holds"]]
        if counterexamples:
            first_failing_seed = seeds[trials.index(next(trial for trial in trials if not trial["conjecture_holds"]))]
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=no_counterexamples")