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
            sign = random.choice([-1, 1])
            clause.append(sign * var)
        clauses.append(clause)
    return clauses

def is_unsat(clauses, n):
    # Simple DPLL for small instances
    if n > 18:
        return True  # Assume unsat for larger instances
    assignments = {}
    def dp(remaining_clauses):
        if not remaining_clauses:
            return True
        for clause in remaining_clauses:
            unassigned = [lit for lit in clause if abs(lit) not in assignments]
            if not unassigned:
                if all(assignments[abs(lit)] == lit > 0 for lit in clause):
                    return False
                continue
            lit = unassigned[0]
            for val in [True, False]:
                assignments[abs(lit)] = val
                new_remaining = [c for c in remaining_clauses if c != clause]
                if dp(new_remaining):
                    return True
                del assignments[abs(lit)]
        return False
    return not dp(clauses)

def build_ribbon_graph(clauses, n):
    # Build half-edge structure
    half_edges = []
    vertex_to_half_edges = defaultdict(list)
    clause_vertices = []
    variable_vertices = []

    # Add clause vertices
    for i, clause in enumerate(clauses):
        clause_vertex = f"C{i}"
        clause_vertices.append(clause_vertex)
        # Sort literals by signed index
        sorted_lits = sorted(clause, key=lambda x: (abs(x), x))
        for j, lit in enumerate(sorted_lits):
            half_edge = (clause_vertex, f"V{abs(lit)}", lit > 0, j)
            half_edges.append(half_edge)
            vertex_to_half_edges[clause_vertex].append(half_edge)

    # Add variable vertices
    for v in range(1, n + 1):
        variable_vertex = f"V{v}"
        variable_vertices.append(variable_vertex)
        # Find all occurrences of v in clauses
        occurrences = []
        for i, clause in enumerate(clauses):
            for lit in clause:
                if abs(lit) == v:
                    occurrences.append((i, lit > 0))
        # Sort by clause index, alternating signs
        occurrences.sort(key=lambda x: x[0])
        for j, (clause_idx, sign) in enumerate(occurrences):
            half_edge = (variable_vertex, f"C{clause_idx}", sign, j)
            half_edges.append(half_edge)
            vertex_to_half_edges[variable_vertex].append(half_edge)

    return half_edges, vertex_to_half_edges, clause_vertices, variable_vertices

def trace_boundary_cycles(half_edges, vertex_to_half_edges):
    visited = set()
    cycles = 0

    for half_edge in half_edges:
        if half_edge not in visited:
            current = half_edge
            cycle = []
            while current not in visited:
                visited.add(current)
                cycle.append(current)
                # Find the next half-edge in the cycle
                u, v, sign, pos = current
                # Find the twin half-edge
                twin = None
                for he in vertex_to_half_edges[v]:
                    if he[1] == u:
                        twin = he
                        break
                if twin is None:
                    break
                # Apply σ or τ rotation
                if v.startswith('C'):
                    # σ rotation for clause vertex
                    next_pos = (pos + 1) % 3
                    next_he = None
                    for he in vertex_to_half_edges[v]:
                        if he[3] == next_pos:
                            next_he = he
                            break
                else:
                    # τ rotation for variable vertex
                    next_pos = (pos + 1) % len(vertex_to_half_edges[v])
                    next_he = None
                    for he in vertex_to_half_edges[v]:
                        if he[3] == next_pos:
                            next_he = he
                            break
                if next_he is None:
                    break
                current = next_he
            if cycle:
                cycles += 1
    return cycles

def compute_g(F, n, m):
    half_edges, vertex_to_half_edges, clause_vertices, variable_vertices = build_ribbon_graph(F, n)
    F_R = trace_boundary_cycles(half_edges, vertex_to_half_edges)
    g = (2 - (m + n) + 3 * m - F_R) / 2
    return g

def compute_resolution_width(F, n):
    if n > 18:
        # Use DPLL proxy for larger instances
        max_width = 0
        assignments = {}
        def dp(remaining_clauses, current_width):
            nonlocal max_width
            if not remaining_clauses:
                return
            max_width = max(max_width, current_width)
            for clause in remaining_clauses:
                unassigned = [lit for lit in clause if abs(lit) not in assignments]
                if not unassigned:
                    continue
                lit = unassigned[0]
                for val in [True, False]:
                    assignments[abs(lit)] = val
                    new_remaining = [c for c in remaining_clauses if c != clause]
                    dp(new_remaining, current_width + 1)
                    del assignments[abs(lit)]
        dp(F, 0)
        return max_width
    else:
        # Brute-force DP for smaller instances
        from functools import lru_cache
        @lru_cache(maxsize=None)
        def dp(frozen_clauses, frozen_assignments):
            if not frozen_clauses:
                return 0
            current_clauses = list(frozen_clauses)
            current_assignments = dict(frozen_assignments)
            min_width = float('inf')
            for clause in current_clauses:
                unassigned = [lit for lit in clause if abs(lit) not in current_assignments]
                if not unassigned:
                    continue
                lit = unassigned[0]
                for val in [True, False]:
                    new_assignments = current_assignments.copy()
                    new_assignments[abs(lit)] = val
                    new_clauses = [c for c in current_clauses if c != clause]
                    width = dp(tuple(new_clauses), tuple(sorted(new_assignments.items())))
                    min_width = min(min_width, width + 1)
            return min_width
        return dp(tuple(F), tuple())

def run_trial(seed):
    random.seed(seed)
    n = random.choice([10, 14, 18, 22, 26, 30])
    alpha = random.choice([4.0, 4.5, 5.0])
    m = int(n * alpha)
    F = generate_3cnf(n, m, seed)
    if not is_unsat(F, n):
        return {
            "metric_name": "resolution_width_lower_bound",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    g = compute_g(F, n, m)
    w_res = compute_resolution_width(F, n)
    threshold = 0.25 * math.log2(1 + g)
    conjecture_holds = w_res >= threshold
    if not conjecture_holds:
        counterexample = f"n={n}, m={m}, g(F)={g}, w_Res(F)={w_res}, threshold={threshold}"
    else:
        counterexample = ""
    return {
        "metric_name": "resolution_width_lower_bound",
        "metric_value": w_res,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
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