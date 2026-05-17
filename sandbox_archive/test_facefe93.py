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
        clause = []
        for _ in range(3):
            var = random.choice(variables)
            sign = random.choice([1, -1])
            clause.append((sign, var))
        clauses.append(clause)
    return clauses

def is_unsat(clauses, max_depth=10):
    def dpll(clauses, assignments, depth):
        if depth > max_depth:
            return False
        if not clauses:
            return True
        for clause in clauses:
            if all((sign == 1 and var not in assignments) or (sign == -1 and -var not in assignments) for sign, var in clause):
                continue
            if any((sign == 1 and -var in assignments) or (sign == -1 and var in assignments) for sign, var in clause):
                continue
            for sign, var in clause:
                if (sign == 1 and var not in assignments) or (sign == -1 and -var not in assignments):
                    new_assignments = assignments.copy()
                    new_assignments.add(sign * var)
                    new_clauses = [c for c in clauses if not any((s == 1 and v == sign * var) or (s == -1 and v == -sign * var) for s, v in c)]
                    if dpll(new_clauses, new_assignments, depth + 1):
                        return True
            return False
        return True

    return dpll(clauses, set(), 0)

def build_ribbon_graph(clauses, n):
    half_edges = []
    vertex_to_half_edges = defaultdict(list)
    for i, clause in enumerate(clauses):
        clause.sort(key=lambda x: (x[0], x[1]))
        for sign, var in clause:
            half_edges.append((i, var, sign))
            vertex_to_half_edges[i].append(len(half_edges) - 1)
            vertex_to_half_edges[var].append(len(half_edges) - 1)

    visited = set()
    cycles = 0
    for start in range(len(half_edges)):
        if start not in visited:
            current = start
            cycle = []
            while True:
                if current in visited:
                    break
                visited.add(current)
                cycle.append(current)
                u, v, s = half_edges[current]
                next_vertex = v if u == vertex_to_half_edges[u][0] // 2 else u
                next_half_edge = vertex_to_half_edges[next_vertex][(vertex_to_half_edges[next_vertex].index(current) + 1) % len(vertex_to_half_edges[next_vertex])]
                current = next_half_edge
            if cycle:
                cycles += 1
    m = len(clauses)
    g = (2 - (m + n) + 3 * m - cycles) / 2
    return g

def compute_resolution_width(clauses, n):
    if n > 18:
        return compute_dpll_width(clauses)
    else:
        return compute_dp_width(clauses)

def compute_dp_width(clauses):
    width = 0
    for clause in clauses:
        width = max(width, len(clause))
    return width

def compute_dpll_width(clauses):
    def dpll_width(clauses, assignments, current_width):
        if not clauses:
            return current_width
        for clause in clauses:
            if all((sign == 1 and var not in assignments) or (sign == -1 and -var not in assignments) for sign, var in clause):
                continue
            if any((sign == 1 and -var in assignments) or (sign == -1 and var in assignments) for sign, var in clause):
                continue
            for sign, var in clause:
                if (sign == 1 and var not in assignments) or (sign == -1 and -var not in assignments):
                    new_assignments = assignments.copy()
                    new_assignments.add(sign * var)
                    new_clauses = [c for c in clauses if not any((s == 1 and v == sign * var) or (s == -1 and v == -sign * var) for s, v in c)]
                    current_width = max(current_width, len(clause))
                    current_width = dpll_width(new_clauses, new_assignments, current_width)
            return current_width
        return current_width

    return dpll_width(clauses, set(), 0)

def run_trial(seed):
    n_values = [10, 14, 18, 22, 26, 30]
    alpha_values = [4.0, 4.5, 5.0]
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for alpha in alpha_values:
            m = int(alpha * n)
            clauses = generate_3cnf(n, m, seed)
            if is_unsat(clauses):
                g = build_ribbon_graph(clauses, n)
                w_res = compute_resolution_width(clauses, n)
                metric_value = w_res / (0.25 * math.log2(1 + g)) if g > 0 else float('inf')
                metric_values.append(metric_value)
                instances_tested += 1
                if metric_value < 1:
                    conjecture_holds = False
                    counterexample = f"n={n}, alpha={alpha}, w_res={w_res}, g={g}"
                    break
        if not conjecture_holds:
            break

    if instances_tested == 0:
        return {
            "metric_name": "w_res / (0.25 * log2(1 + g))",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    return {
        "metric_name": "w_res / (0.25 * log2(1 + g))",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    seeds = [int(seed) for seed in seeds]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    conjecture_holds = [r["conjecture_holds"] for r in results if r["instances_tested"] > 0]
    counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
    elif any(not holds for holds in conjecture_holds):
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[conjecture_holds.index(False)]}")
    else:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(conjecture_holds) / len(conjecture_holds)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")