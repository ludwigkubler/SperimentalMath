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
        raise ValueError("n must be even for 3-regular graphs")
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    remaining_vertices = list(range(n))
    while remaining_vertices:
        u = remaining_vertices.pop()
        neighbors = [v for v in vertices if (u, v) in edges or (v, u) in edges]
        if len(neighbors) >= 3:
            continue
        candidates = [v for v in vertices if v != u and v not in neighbors]
        if not candidates:
            continue
        v = random.choice(candidates)
        edges.append((u, v))
    return edges

def is_odd_sum_charge(G, c):
    n = len(set(itertools.chain.from_iterable(G)))
    return sum(c[v] for v in range(n)) % 2 != 0

def generate_odd_sum_charge(n):
    c = [random.randint(0, 1) for _ in range(n)]
    while sum(c) % 2 == 0:
        c[random.randint(0, n-1)] ^= 1
    return c

def matching_polynomial(G):
    n = len(set(itertools.chain.from_iterable(G)))
    mu = [0] * (n + 1)
    mu[n] = 1
    for k in range(n, 0, -1):
        for edge in G:
            u, v = edge
            if mu[k] != 0:
                mu[k-2] += mu[k]
    return mu

def mahler_measure(mu):
    roots = []
    for k in range(len(mu)):
        if mu[k] != 0:
            roots.extend([1] * mu[k])
    M = 1.0
    for r in roots:
        if abs(r) >= 1:
            M *= abs(r)
    return M

def generate_cnf(G, c):
    n = len(set(itertools.chain.from_iterable(G)))
    clauses = []
    for edge in G:
        u, v = edge
        clauses.append([u, v])
        clauses.append([-u, -v])
    for v in range(n):
        if c[v] == 1:
            clauses.append([v])
        else:
            clauses.append([-v])
    return clauses

def dpll(clauses, assignment, order):
    if not clauses:
        return 1
    for clause in clauses:
        if all(lit == 0 for lit in clause):
            return 0
    if not order:
        return 1
    var = order.pop(0)
    for val in [1, -1]:
        new_assignment = assignment.copy()
        new_assignment[var] = val
        new_clauses = []
        for clause in clauses:
            new_clause = []
            for lit in clause:
                if lit == var * val:
                    new_clause = []
                    break
                elif lit != -var * val:
                    new_clause.append(lit)
            if new_clause:
                new_clauses.append(new_clause)
        result = dpll(new_clauses, new_assignment, order.copy())
        if result != 0:
            return result + 1
    return 0

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(30):
            G = generate_3_regular_graph(n)
            c = generate_odd_sum_charge(n)
            mu_G = matching_polynomial(G)
            M = mahler_measure(mu_G)
            clauses = generate_cnf(G, c)
            order = list(range(n))
            random.shuffle(order)
            T = dpll(clauses, {}, order.copy())
            metric_value = math.log2(T) if T > 0 else 0
            metric_values.append(metric_value)
            instances_tested += 1
            if metric_value < math.log2(M) - 1:
                conjecture_holds = False
                counterexample = f"n={n}, T={T}, M={M}"
                break
        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "log2_T_minus_log2_M",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2_T_minus_log2_M",
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
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]
        counterexample = results[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=0")